#!/usr/bin/env python3
"""
MCP Document Analyzer Server

This is a Model Context Protocol (MCP) server that provides document analysis capabilities.
It implements the MCP specification to allow AI assistants to analyze text documents
for sentiment, keywords, readability, and basic statistics.

The MCP protocol is a simple JSON-based protocol that allows AI assistants to interact
with external tools and data sources in a standardized way.
"""

import json
import os
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import logging
from datetime import datetime
from document_analyzer import DocumentAnalyzer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MCPHandler(BaseHTTPRequestHandler):
    """
    HTTP request handler for MCP protocol.
    
    The Model Context Protocol (MCP) is a simple protocol that allows
    AI assistants to interact with external tools and data sources.
    
    This handler processes MCP requests and routes them to appropriate
    document analysis functions.
    """
    
    def __init__(self, *args, **kwargs):
        # Initialize document analyzer
        self.analyzer = DocumentAnalyzer()
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Handle GET requests - mainly for health checks and tool discovery."""
        parsed_url = urlparse(self.path)
        
        if parsed_url.path == '/health':
            self._send_response(200, {"status": "healthy", "message": "MCP Document Analyzer Server is running"})
        elif parsed_url.path == '/tools':
            # Return available MCP tools
            tools = self._get_available_tools()
            self._send_response(200, {"tools": tools})
        else:
            self._send_response(404, {"error": "Endpoint not found"})
    
    def do_POST(self):
        """Handle POST requests - main MCP tool execution."""
        try:
            # Read request body
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            
            # Parse JSON request
            request_data = json.loads(body)
            
            # Extract MCP request components
            tool_name = request_data.get('tool')
            arguments = request_data.get('arguments', {})
            
            logger.info(f"MCP Request: {tool_name} with arguments: {arguments}")
            
            # Route to appropriate tool handler
            if tool_name == 'analyze_document':
                result = self._handle_analyze_document(arguments)
            elif tool_name == 'get_sentiment':
                result = self._handle_get_sentiment(arguments)
            elif tool_name == 'extract_keywords':
                result = self._handle_extract_keywords(arguments)
            elif tool_name == 'add_document':
                result = self._handle_add_document(arguments)
            elif tool_name == 'search_documents':
                result = self._handle_search_documents(arguments)
            else:
                result = {"error": f"Unknown tool: {tool_name}"}
                self._send_response(400, result)
                return
            
            # Send successful response
            self._send_response(200, {
                "tool": tool_name,
                "result": result,
                "timestamp": datetime.now().isoformat()
            })
            
        except json.JSONDecodeError:
            self._send_response(400, {"error": "Invalid JSON in request body"})
        except Exception as e:
            logger.error(f"Error processing MCP request: {str(e)}")
            self._send_response(500, {"error": f"Internal server error: {str(e)}"})
    
    def _send_response(self, status_code, data):
        """Send JSON response with proper headers."""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        response_json = json.dumps(data, indent=2, ensure_ascii=False)
        self.wfile.write(response_json.encode('utf-8'))
    
    def do_OPTIONS(self):
        """Handle OPTIONS requests for CORS."""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def _get_available_tools(self):
        """Return list of available MCP tools with their descriptions."""
        return [
            {
                "name": "analyze_document",
                "description": "Perform complete analysis of a document including sentiment, keywords, readability, and statistics",
                "parameters": {
                    "document_id": {
                        "type": "string",
                        "description": "ID of the document to analyze",
                        "required": True
                    }
                }
            },
            {
                "name": "get_sentiment",
                "description": "Analyze sentiment of any text (positive/negative/neutral)",
                "parameters": {
                    "text": {
                        "type": "string",
                        "description": "Text to analyze for sentiment",
                        "required": True
                    }
                }
            },
            {
                "name": "extract_keywords",
                "description": "Extract top keywords from text",
                "parameters": {
                    "text": {
                        "type": "string",
                        "description": "Text to extract keywords from",
                        "required": True
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of keywords to return (default: 10)",
                        "required": False,
                        "default": 10
                    }
                }
            },
            {
                "name": "add_document",
                "description": "Add a new document to the collection",
                "parameters": {
                    "document_data": {
                        "type": "object",
                        "description": "Document data including content, title, author, and category",
                        "required": True,
                        "properties": {
                            "content": {"type": "string", "description": "Document content"},
                            "title": {"type": "string", "description": "Document title"},
                            "author": {"type": "string", "description": "Document author"},
                            "category": {"type": "string", "description": "Document category"}
                        }
                    }
                }
            },
            {
                "name": "search_documents",
                "description": "Search documents by content or metadata",
                "parameters": {
                    "query": {
                        "type": "string",
                        "description": "Search query",
                        "required": True
                    }
                }
            }
        ]
    
    def _handle_analyze_document(self, arguments):
        """Handle analyze_document tool request."""
        document_id = arguments.get('document_id')
        if not document_id:
            return {"error": "document_id is required"}
        
        try:
            result = self.analyzer.analyze_document(document_id)
            return result
        except ValueError as e:
            return {"error": str(e)}
    
    def _handle_get_sentiment(self, arguments):
        """Handle get_sentiment tool request."""
        text = arguments.get('text')
        if not text:
            return {"error": "text is required"}
        
        try:
            result = self.analyzer.get_sentiment(text)
            return result
        except Exception as e:
            return {"error": f"Sentiment analysis failed: {str(e)}"}
    
    def _handle_extract_keywords(self, arguments):
        """Handle extract_keywords tool request."""
        text = arguments.get('text')
        limit = arguments.get('limit', 10)
        
        if not text:
            return {"error": "text is required"}
        
        try:
            result = self.analyzer.extract_keywords(text, limit)
            return {"keywords": result}
        except Exception as e:
            return {"error": f"Keyword extraction failed: {str(e)}"}
    
    def _handle_add_document(self, arguments):
        """Handle add_document tool request."""
        document_data = arguments.get('document_data')
        if not document_data:
            return {"error": "document_data is required"}
        
        try:
            document_id = self.analyzer.add_document(document_data)
            return {
                "document_id": document_id,
                "message": "Document added successfully"
            }
        except Exception as e:
            return {"error": f"Failed to add document: {str(e)}"}
    
    def _handle_search_documents(self, arguments):
        """Handle search_documents tool request."""
        query = arguments.get('query')
        if not query:
            return {"error": "query is required"}
        
        try:
            results = self.analyzer.search_documents(query)
            return {"results": results}
        except Exception as e:
            return {"error": f"Search failed: {str(e)}"}
    
    def log_message(self, format, *args):
        """Override to use our logger instead of stderr."""
        logger.info(f"{self.address_string()} - {format % args}")

def create_sample_documents():
    """Create sample documents for testing."""
    analyzer = DocumentAnalyzer()
    
    # Only create if no documents exist
    if len(analyzer.get_all_documents()) > 0:
        print("Sample documents already exist. Skipping creation.")
        return
    
    print("Creating sample documents...")
    
    sample_docs = [
        {
            "title": "The Future of Artificial Intelligence",
            "author": "Dr. Sarah Chen",
            "category": "Technology",
            "content": """Artificial intelligence has rapidly evolved from a concept in science fiction to a transformative technology that impacts every aspect of our daily lives. Machine learning algorithms now power everything from recommendation systems to autonomous vehicles, fundamentally changing how we interact with technology.

The recent advances in deep learning have enabled computers to perform tasks that were once thought to be exclusively human. Natural language processing allows machines to understand and generate human-like text, while computer vision enables them to interpret and analyze visual information with remarkable accuracy.

However, with these capabilities come significant challenges. Ethical considerations around AI decision-making, privacy concerns, and the potential for job displacement require careful consideration. As we move forward, it's crucial to develop AI systems that are not only powerful but also responsible, transparent, and aligned with human values.

The future of AI holds immense promise. From healthcare diagnostics to climate change mitigation, AI has the potential to solve some of humanity's most pressing challenges. Success will depend on our ability to harness this technology wisely and ensure its benefits are distributed equitably across society."""
        },
        {
            "title": "Climate Change and Ocean Acidification",
            "author": "Prof. Maria Rodriguez",
            "category": "Environment",
            "content": """The world's oceans are experiencing unprecedented changes due to climate change, with ocean acidification emerging as one of the most serious threats to marine ecosystems. As atmospheric carbon dioxide levels continue to rise, the oceans absorb approximately 30% of this excess CO2, leading to a decrease in seawater pH.

This process, often called the 'other CO2 problem,' is happening at a rate not seen in millions of years. The increased acidity makes it difficult for marine organisms like corals, shellfish, and certain plankton to build and maintain their calcium carbonate shells and skeletons.

Coral reefs, which support about 25% of all marine species, are particularly vulnerable. The combination of warming waters and acidification creates a double threat that has already led to widespread coral bleaching events. The Great Barrier Reef, for instance, has experienced multiple mass bleaching events in recent years.

The implications extend far beyond marine life. Ocean acidification threatens global food security, as many communities depend on seafood for protein and livelihoods. Immediate action is needed to reduce carbon emissions and protect these vital ecosystems for future generations."""
        },
        {
            "title": "The Art of Mindful Living",
            "author": "Zen Master Takeshi",
            "category": "Philosophy",
            "content": """In our fast-paced world, the ancient practice of mindfulness offers a pathway to inner peace and clarity. Mindful living is not about escaping reality but about engaging with it more fully, with awareness and intention.

The practice begins with the breath – the simple act of observing each inhalation and exhalation without judgment. This fundamental exercise teaches us to anchor our attention in the present moment, rather than being swept away by thoughts of the past or worries about the future.

Mindfulness extends beyond formal meditation into every aspect of daily life. Whether we're eating, walking, or having a conversation, we can choose to be fully present. This presence transforms ordinary experiences into opportunities for growth and connection.

The benefits of mindful living are well-documented. Regular practice reduces stress, improves emotional regulation, and enhances overall well-being. More importantly, it cultivates compassion – both for ourselves and others – creating a foundation for more meaningful relationships and a more harmonious society.

True mindfulness is not a destination but a journey. Each moment offers a fresh opportunity to awaken to the richness of life that surrounds us."""
        },
        {
            "title": "Quantum Computing: A Revolutionary Leap",
            "author": "Dr. James Liu",
            "category": "Technology",
            "content": """Quantum computing represents one of the most significant technological breakthroughs of the 21st century. Unlike classical computers that use bits to process information in binary states of 0 or 1, quantum computers use quantum bits or 'qubits' that can exist in multiple states simultaneously through a phenomenon called superposition.

This quantum property, combined with entanglement and interference, allows quantum computers to process vast amounts of information in parallel. For certain types of problems, this provides an exponential advantage over classical computing approaches.

The applications are revolutionary. In cryptography, quantum computers could break current encryption methods while enabling new forms of quantum-secure communication. In drug discovery, they could simulate molecular interactions at an unprecedented scale, accelerating the development of new medications.

However, quantum computing faces significant challenges. Quantum states are extremely fragile and susceptible to environmental interference, requiring sophisticated error correction and operating at near absolute zero temperatures. Current quantum computers are still in their infancy, with limited practical applications.

Despite these challenges, major technology companies and research institutions are investing heavily in quantum research. The race to achieve 'quantum supremacy' – the point where quantum computers can solve problems impossible for classical computers – is intensifying, promising to reshape computing as we know it."""
        },
        {
            "title": "The Psychology of Happiness",
            "author": "Dr. Emma Thompson",
            "category": "Psychology",
            "content": """Happiness is one of humanity's most pursued yet elusive goals. Modern psychology has made significant strides in understanding what contributes to genuine well-being and life satisfaction.

Research shows that happiness is not simply the absence of negative emotions but the presence of positive ones, combined with a sense of meaning and purpose. The field of positive psychology has identified several key factors that contribute to happiness: positive relationships, engagement in meaningful activities, accomplishment, and gratitude.

Contrary to popular belief, external circumstances like wealth, fame, or material possessions have a surprisingly limited impact on long-term happiness. The 'hedonic treadmill' explains how people quickly adapt to positive changes in their circumstances, returning to baseline levels of happiness.

Instead, sustainable happiness comes from internal factors and practices. Regular exercise, meditation, acts of kindness, and maintaining strong social connections have been shown to have lasting positive effects on well-being. The practice of gratitude – actively acknowledging and appreciating the good things in life – is particularly powerful.

Understanding the psychology of happiness empowers us to make choices that truly enhance our well-being rather than chasing temporary pleasures that ultimately leave us unsatisfied."""
        },
        {
            "title": "Sustainable Agriculture and Food Security",
            "author": "Dr. Michael Green",
            "category": "Agriculture",
            "content": """As the global population approaches 10 billion by 2050, ensuring food security while protecting our environment has become one of the most critical challenges of our time. Traditional industrial agriculture, while successful in increasing yields, has come at a significant environmental cost.

Sustainable agriculture offers a promising alternative that balances productivity with environmental stewardship. This approach emphasizes soil health, biodiversity conservation, and reduced reliance on synthetic inputs. Practices such as crop rotation, cover cropping, and integrated pest management help maintain ecosystem balance while producing nutritious food.

Precision agriculture, enabled by modern technology, allows farmers to optimize resource use through GPS-guided equipment, soil sensors, and data analytics. This technology-driven approach reduces waste, minimizes environmental impact, and can actually increase yields compared to conventional methods.

Urban agriculture and vertical farming represent innovative solutions for growing food in limited spaces. These systems can produce fresh produce year-round with minimal water usage and no pesticides, bringing food production closer to consumers and reducing transportation costs.

The transition to sustainable agriculture requires support from policymakers, consumers, and the agricultural industry. By choosing sustainably produced food and supporting farmers who adopt these practices, we can create a food system that nourishes both people and the planet."""
        },
        {
            "title": "The Digital Divide and Social Equity",
            "author": "Prof. Lisa Chang",
            "category": "Social Issues",
            "content": """The digital divide – the gap between those who have access to modern information and communication technologies and those who don't – has become a critical social justice issue in the 21st century. This divide affects not just access to technology but access to opportunities, education, healthcare, and economic participation.

The COVID-19 pandemic starkly highlighted these inequalities. While many people could work from home and students could attend virtual classes, millions were left behind due to lack of internet access, digital devices, or digital literacy skills. This digital exclusion exacerbated existing social and economic inequalities.

The divide exists at multiple levels: between developed and developing countries, between urban and rural areas, and between different socioeconomic groups within the same community. Factors such as income, education, age, and geographic location all influence digital access and usage.

Addressing the digital divide requires comprehensive solutions. Infrastructure development to expand broadband access, especially in underserved areas, is crucial. Equally important are digital literacy programs that teach people how to effectively use technology for education, employment, and civic participation.

Public-private partnerships, community initiatives, and government policies all play vital roles in bridging this divide. As our world becomes increasingly digital, ensuring equitable access to technology is not just a matter of convenience but a fundamental requirement for social justice and economic opportunity."""
        },
        {
            "title": "Space Exploration: The Next Frontier",
            "author": "Dr. Robert NASA",
            "category": "Science",
            "content": """Space exploration has entered a new era of unprecedented activity and innovation. With private companies joining government agencies in the quest to explore the cosmos, we are witnessing a renaissance in space technology and ambition.

The recent success of reusable rockets has dramatically reduced the cost of space access, making previously impossible missions economically viable. Companies like SpaceX, Blue Origin, and Virgin Galactic are pioneering new approaches to space travel, while established space agencies continue to push the boundaries of scientific discovery.

Mars exploration has captured global imagination, with multiple missions currently studying the Red Planet. The search for signs of past or present life on Mars could answer one of humanity's most profound questions: Are we alone in the universe? Plans for human missions to Mars are no longer science fiction but serious engineering challenges being actively addressed.

Beyond Mars, missions to the outer planets and their moons are revealing the incredible diversity of our solar system. Jupiter's moon Europa and Saturn's moon Enceladus, with their subsurface oceans, represent potential habitats for life as we know it.

Space exploration also drives technological innovation that benefits life on Earth. Satellite technology enables GPS navigation, weather forecasting, and global communications. Materials and technologies developed for space missions often find applications in medicine, manufacturing, and environmental monitoring.

As we stand on the threshold of becoming a multi-planetary species, space exploration represents not just scientific curiosity but a potential safeguard for human civilization and a source of inspiration for future generations."""
        },
        {
            "title": "The Renaissance of Vinyl Records",
            "author": "Music Historian Alex Smith",
            "category": "Culture",
            "content": """In an age of digital streaming and instant access to millions of songs, an unexpected phenomenon has emerged: the resurgence of vinyl records. Once declared obsolete, vinyl has experienced a remarkable renaissance, with sales reaching levels not seen since the 1980s.

This revival goes beyond mere nostalgia. Vinyl offers a tangible, ritualistic experience that digital formats cannot replicate. The act of selecting a record, placing it on the turntable, and experiencing the warm, analog sound creates a deeper connection between listener and music.

Audiophiles argue that vinyl provides superior sound quality, with its analog format capturing nuances that digital compression might miss. The larger format also allows for elaborate artwork and liner notes, transforming albums into collectible art pieces.

The vinyl revival has had significant impacts on the music industry. Artists now consider vinyl releases as essential parts of their marketing strategy, often creating special editions and limited releases that generate excitement among fans. Record stores, once endangered, have found new life as cultural hubs for music discovery and community gathering.

This trend reflects a broader cultural shift toward valuing authentic, tactile experiences in our increasingly digital world. Just as craft beer and artisanal foods have gained popularity, vinyl represents a return to the craftsmanship and intentionality that mass production often lacks.

The vinyl renaissance demonstrates that technology doesn't always move in a linear direction. Sometimes, the 'old' ways offer something valuable that the new cannot replace."""
        },
        {
            "title": "Renewable Energy Revolution",
            "author": "Dr. Patricia Solar",
            "category": "Environment",
            "content": """The transition to renewable energy is accelerating at an unprecedented pace, driven by technological advances, falling costs, and growing environmental awareness. Solar and wind power, once considered alternative energy sources, are now the cheapest forms of electricity generation in many parts of the world.

Solar technology has experienced dramatic improvements in efficiency and cost reduction. Modern solar panels can convert over 20% of sunlight into electricity, while costs have dropped by more than 80% over the past decade. This has made solar power accessible to homeowners, businesses, and utilities alike.

Wind energy has similarly transformed, with modern turbines generating more power from less wind. Offshore wind farms, in particular, offer enormous potential due to stronger and more consistent winds at sea. Countries like Denmark and Germany have demonstrated that high percentages of renewable energy in the grid are not only possible but economically advantageous.

Energy storage technology is solving the intermittency challenge of renewables. Advanced battery systems can store excess energy generated during peak production times for use when the sun isn't shining or the wind isn't blowing. This technological breakthrough is making renewable energy more reliable and practical.

The renewable energy revolution extends beyond environmental benefits. It's creating new industries, jobs, and economic opportunities while reducing dependence on fossil fuel imports. Countries that invest heavily in renewable energy are positioning themselves as leaders in the global clean energy economy.

The transformation is not without challenges, but the momentum is undeniable. The renewable energy revolution represents one of the most significant technological and economic shifts of our time."""
        },
        {
            "title": "The Science of Sleep",
            "author": "Dr. Matthew Dream",
            "category": "Health",
            "content": """Sleep, once considered a passive state of rest, is now understood to be an active and crucial process for physical health, mental well-being, and cognitive function. Modern sleep research has revealed the intricate mechanisms that govern our sleep-wake cycles and the profound consequences of sleep deprivation.

During sleep, our brains engage in essential maintenance activities. The glymphatic system, discovered relatively recently, clears metabolic waste from brain cells, including proteins associated with Alzheimer's disease. This 'neural housekeeping' function explains why chronic sleep deprivation is linked to cognitive decline and neurodegenerative diseases.

Sleep occurs in distinct stages, each serving different functions. Deep sleep is crucial for physical recovery and memory consolidation, while REM sleep plays a vital role in emotional processing and creativity. The complete sleep cycle, typically lasting 90 minutes, repeats multiple times throughout the night.

Modern lifestyle factors significantly impact sleep quality. Blue light from electronic devices can disrupt our circadian rhythms by suppressing melatonin production. Caffeine, consumed even six hours before bedtime, can interfere with sleep onset and quality. Stress and anxiety create a vicious cycle where poor sleep exacerbates mental health issues, which in turn worsen sleep problems.

The consequences of sleep deprivation extend far beyond feeling tired. Chronic sleep loss is associated with increased risk of obesity, diabetes, cardiovascular disease, and weakened immune function. Even short-term sleep deprivation impairs decision-making, reaction time, and emotional regulation.

Understanding sleep science empowers us to prioritize this fundamental biological need. Good sleep hygiene – maintaining consistent sleep schedules, creating optimal sleep environments, and managing stress – is as important as diet and exercise for overall health."""
        },
        {
            "title": "The Future of Work in the Digital Age",
            "author": "Labor Economist Dr. Jennifer Future",
            "category": "Economics",
            "content": """The nature of work is undergoing a fundamental transformation driven by technological advancement, changing demographics, and evolving worker expectations. The traditional model of full-time employment with a single employer for decades is giving way to more flexible, diverse, and dynamic work arrangements.

Automation and artificial intelligence are reshaping job markets across industries. While some jobs are being eliminated, new roles are emerging that require different skills. The key is not whether technology will replace human workers, but how humans and machines will collaborate to create value.

Remote work, accelerated by the COVID-19 pandemic, has proven that many jobs can be performed effectively from anywhere. This shift has implications for urban planning, real estate markets, and work-life balance. Companies are discovering that remote work can increase productivity while reducing overhead costs.

The gig economy continues to grow, offering workers flexibility and autonomy while also creating new challenges around benefits, job security, and worker rights. Platforms like Uber, Airbnb, and freelance marketplaces have created new forms of entrepreneurship and income generation.

Skills-based hiring is becoming more important than traditional credentials. Employers are increasingly valuing demonstrated abilities over formal education, leading to the rise of alternative learning platforms and micro-credentials. Continuous learning and adaptation are becoming essential for career success.

The future workplace will likely be characterized by greater flexibility, emphasis on well-being, and focus on meaningful work. Organizations that adapt to these changing expectations while leveraging technology effectively will thrive in the new economy."""
        },
        {
            "title": "Urban Gardening and Community Building",
            "author": "Community Organizer Maria Roots",
            "category": "Community",
            "content": """Urban gardening has emerged as a powerful tool for community building, environmental sustainability, and food security in cities around the world. What began as a necessity during economic hardship has evolved into a movement that transforms neighborhoods and connects people to their food and each other.

Community gardens provide fresh produce in areas often classified as food deserts, where access to healthy, affordable food is limited. These spaces not only improve nutrition but also reduce food costs for participants, making healthy eating more accessible to low-income families.

The benefits extend far beyond food production. Urban gardens serve as gathering spaces where neighbors meet, share knowledge, and build social connections. They provide opportunities for intergenerational learning, where experienced gardeners mentor newcomers and cultural food traditions are preserved and shared.

Children who participate in urban gardening programs develop better eating habits, learn about nutrition and environmental science, and gain valuable life skills. Schools with garden programs report improved student engagement and academic performance, particularly in science subjects.

Urban gardens also contribute to environmental sustainability. They reduce the urban heat island effect, improve air quality, and manage stormwater runoff. Composting programs associated with many gardens divert organic waste from landfills while creating nutrient-rich soil amendments.

The movement faces challenges including land access, funding, and seasonal limitations in colder climates. However, innovative solutions like vertical gardening, hydroponics, and year-round growing facilities are expanding possibilities for urban food production.

Urban gardening represents a grassroots approach to addressing multiple urban challenges simultaneously: food security, community cohesion, environmental sustainability, and public health."""
        },
        {
            "title": "The Ethics of Genetic Engineering",
            "author": "Bioethicist Dr. Helen Genes",
            "category": "Ethics",
            "content": """Genetic engineering technologies, particularly CRISPR-Cas9, have given humanity unprecedented power to modify the genetic code of living organisms. This capability raises profound ethical questions that society must grapple with as these technologies become more accessible and powerful.

The potential benefits are enormous. Gene therapy could cure genetic diseases that have plagued humanity for millennia. Crops could be engineered to be more nutritious, drought-resistant, and capable of growing in challenging environments, addressing food security in a changing climate.

However, the power to edit genes also raises serious concerns. The distinction between therapeutic applications and enhancement becomes blurred when we consider genetic modifications that could improve human capabilities beyond normal ranges. Who decides what constitutes an improvement versus a necessary medical intervention?

Germline editing – modifications that can be passed to future generations – is particularly controversial. While it could prevent hereditary diseases, it also raises questions about consent from future generations and the potential for creating genetic inequalities in society.

The accessibility of genetic engineering technology is another ethical consideration. If genetic enhancements become available but expensive, they could exacerbate existing social inequalities. The prospect of a 'genetic divide' between those who can afford enhancements and those who cannot is deeply troubling.

International cooperation and regulation are essential as genetic engineering capabilities advance. The actions of one country or institution can have global implications, making international ethical standards and oversight mechanisms crucial.

As we stand at the threshold of the genetic age, we must proceed with careful consideration of the ethical implications while not allowing fear to prevent beneficial applications that could reduce human suffering."""
        },
        {
            "title": "The Power of Storytelling in Human Culture",
            "author": "Anthropologist Dr. Sarah Narrative",
            "category": "Culture",
            "content": """Storytelling is perhaps humanity's most distinctive and powerful cultural tool. From ancient cave paintings to modern digital media, stories have shaped human civilization, transmitted knowledge, and created shared meaning across generations and cultures.

Stories serve multiple functions in human society. They preserve historical knowledge, teaching lessons about survival, social cooperation, and moral behavior. Myths and legends encode cultural values and provide frameworks for understanding complex concepts like justice, love, and sacrifice.

The human brain appears to be wired for narrative. We naturally organize information into story structures with beginnings, middles, and ends. This narrative thinking helps us make sense of complex events, predict future outcomes, and understand cause-and-effect relationships.

Modern research reveals that stories have profound psychological effects. When we hear stories, our brains release oxytocin, a hormone associated with empathy and social bonding. This biological response explains why stories are so effective at building connections between people and promoting prosocial behavior.

In the digital age, storytelling has evolved but remains central to human communication. Social media platforms are essentially storytelling tools, allowing people to craft and share narratives about their lives. Brands use storytelling to create emotional connections with consumers, while political movements use narratives to mobilize support.

The democratization of storytelling tools means that more voices can participate in shaping cultural narratives. However, this also raises questions about truth, authenticity, and the responsibility that comes with the power to influence others through stories.

Understanding the power of storytelling helps us become more critical consumers of information while appreciating the profound role that narratives play in shaping human experience and society."""
        },
        {
            "title": "Cryptocurrency and the Future of Money",
            "author": "Financial Analyst Dr. Bitcoin Cash",
            "category": "Finance",
            "content": """Cryptocurrency has emerged from obscurity to become a significant force in global finance, challenging traditional notions of money, banking, and financial sovereignty. What began as an experimental digital currency has evolved into a diverse ecosystem of financial innovations.

Bitcoin, the first cryptocurrency, introduced the concept of decentralized digital money backed by cryptographic proof rather than government authority. Its blockchain technology creates a permanent, transparent ledger of all transactions without requiring a central authority to verify or process payments.

The implications extend far beyond digital payments. Smart contracts, enabled by platforms like Ethereum, allow for programmable money that can automatically execute agreements when predetermined conditions are met. This technology has applications in insurance, supply chain management, and decentralized finance (DeFi).

Cryptocurrency offers particular advantages in developing countries where traditional banking infrastructure is limited. Digital currencies can provide financial services to the unbanked population, enable cross-border remittances at lower costs, and protect against currency devaluation.

However, cryptocurrency faces significant challenges. Price volatility makes it difficult to use as a stable medium of exchange. Energy consumption, particularly for Bitcoin mining, raises environmental concerns. Regulatory uncertainty creates risks for investors and businesses.

Central banks are responding by developing their own digital currencies (CBDCs), attempting to capture the benefits of digital money while maintaining government control. This development could reshape the relationship between citizens and monetary authorities.

The future of money will likely involve a hybrid system where traditional currencies, cryptocurrencies, and central bank digital currencies coexist. Understanding these technologies is crucial for navigating the evolving financial landscape."""
        }
    ]
    
    # Add each sample document
    for doc_data in sample_docs:
        try:
            doc_id = analyzer.add_document(doc_data)
            print(f"Created document {doc_id}: {doc_data['title']}")
        except Exception as e:
            print(f"Error creating document '{doc_data['title']}': {str(e)}")
    
    print(f"\nSuccessfully created {len(sample_docs)} sample documents!")
    print(f"Total documents in collection: {len(analyzer.get_all_documents())}")

def main():
    """Main function to start the MCP server."""
    # Create sample documents if they don't exist
    create_sample_documents()
    
    # Server configuration
    HOST = 'localhost'
    PORT = 8000
    
    # Create and start server
    server = HTTPServer((HOST, PORT), MCPHandler)
    
    print(f"\n{'='*60}")
    print(f"MCP Document Analyzer Server Starting")
    print(f"{'='*60}")
    print(f"Server running on: http://{HOST}:{PORT}")
    print(f"Health check: http://{HOST}:{PORT}/health")
    print(f"Available tools: http://{HOST}:{PORT}/tools")
    print(f"{'='*60}")
    print(f"Available MCP Tools:")
    print(f"  - analyze_document(document_id)")
    print(f"  - get_sentiment(text)")
    print(f"  - extract_keywords(text, limit)")
    print(f"  - add_document(document_data)")
    print(f"  - search_documents(query)")
    print(f"{'='*60}")
    print(f"Press Ctrl+C to stop the server")
    print(f"{'='*60}\n")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        server.shutdown()
        print("Server stopped.")

if __name__ == "__main__":
    main() 