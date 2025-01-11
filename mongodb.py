from pymongo import MongoClient
from datetime import datetime

mongoURI = 'mongodb+srv://actedcone:dualipa@atlascluster.t9cnxbb.mongodb.net/?retryWrites=true&w=majority&appName=AtlasCluster'
client = MongoClient(mongoURI)

db = client.ENCODE

products_collection = db.products
customers_collection = db.customers
calls_collection = db.calls
survey_collection = db.survey

# products_data = [
#     {"name": "Laptop", "id": 1, "price": 1200, "type": "Electronics", "offers": "10% off", "warranty_details": "2 years", "description": "A high-performance laptop with powerful specs for gaming and productivity."},
#     {"name": "Phone", "id": 2, "price": 800, "type": "Electronics", "offers": "5% off", "warranty_details": "1 year", "description": "A sleek and stylish smartphone with a powerful camera and fast performance."},
#     {"name": "Headphones", "id": 3, "price": 150, "type": "Accessories", "offers": "Buy 1 Get 1 Free", "warranty_details": "6 months", "description": "High-quality wireless headphones with noise-canceling features."}
# ]

# customers_data = [
#     {"customer_number": 101, "name": "John Doe", "products": [{"product_id": 1, "date_bought": datetime(2024, 1, 5)}, {"product_id": 2, "date_bought": datetime(2024, 1, 10)}], "customer_id": 1001},
#     {"customer_number": 102, "name": "Jane Smith", "products": [{"product_id": 3, "date_bought": datetime(2024, 1, 8)}], "customer_id": 1002}
# ]

# calls_data = [
#     {"transcribed_call": "Hello, we have a special offer on laptops today.", "score": 0.8, "customer_id": 1001},
#     {"transcribed_call": "Hi, just wanted to let you know about our new phone deals.", "score": 0.4, "customer_id": 1002}
# ]

# survey_data = [
#     {"survey_info": "Survey 1: Customer satisfaction on product quality. Participants rated the product quality from 1 to 5, with an average score of 4.2."},
#     {"survey_info": "Survey 2: Customer feedback on the website's usability. Most participants found the website easy to navigate and suggested adding more product details."},
#     {"survey_info": "Survey 3: Preferences for seasonal offers. Customers preferred 15% off offers, and many suggested extending the promotion period."},
#     {"survey_info": "Survey 4: Interest in loyalty programs. 70% of participants expressed interest in earning points with every purchase."},
#     {"survey_info": "Survey 5: Feedback on customer service experience. Participants rated customer service highly, with an average score of 4.8."}
# ]

# survey_collection.insert_many(survey_data)

# products_data = [
#     {
#         "name": "HP Pavilion Gaming Laptop 15",
#         "id": "HP Pavilion Gaming 15-ec1000AX",
#         "price": 89999,
#         "type": "Electronics",
#         "offers": "10% off with ICICI Credit Card, 5% cashback on Amazon Pay",
#         "warranty_details": "1 year",
#         "description": "The HP Pavilion Gaming Laptop 15 is designed to meet the demands of gamers and creators. Powered by the AMD Ryzen 7 5800H processor (8-core, 16-thread) and equipped with the NVIDIA GeForce GTX 1650 GPU, this laptop delivers smooth gameplay and impressive performance for both gaming and professional workloads. It features a 15.6-inch Full HD display with a 144Hz refresh rate for smooth visuals. The laptop is equipped with 16GB of RAM and a 512GB SSD for fast load times and multitasking. Ideal for gaming, streaming, and content creation, the HP Pavilion 15 provides excellent value for money."
#     },
#     {
#         "name": "Dell XPS 13 (2023) Laptop",
#         "id": "Dell XPS 13 9310",
#         "price": 149999,
#         "type": "Electronics",
#         "offers": "10% off on Debit Cards, 5% Instant Discount on SBI Credit Card",
#         "warranty_details": "2 years",
#         "description": "The Dell XPS 13 (2023) is a premium ultrabook designed for professionals who demand high performance in a compact form. It is powered by the latest 11th Gen Intel Core i7-1165G7 processor, paired with Intel Iris Xe graphics, delivering impressive performance for productivity tasks and light gaming. The 13.4-inch InfinityEdge display offers a 1920x1200 resolution with a 16:10 aspect ratio, providing vibrant visuals and more screen real estate. It comes with 16GB RAM and a 512GB SSD. The build quality is exceptional, featuring a lightweight aluminum chassis and a carbon fiber palm rest for a premium feel."
#     },
#     {
#         "name": "Logitech G Pro X Superlight Wireless Mouse",
#         "id": "Logitech G Pro X",
#         "price": 9999,
#         "type": "Accessories",
#         "offers": "15% off on ICICI Debit Cards",
#         "warranty_details": "1 year",
#         "description": "The Logitech G Pro X Superlight is a high-performance wireless gaming mouse, crafted for esports professionals. With a weight of just 63 grams, it is one of the lightest mice in its category, designed for speed and precision. Equipped with the HERO sensor (25,600 DPI), it ensures ultra-precise tracking with no smoothing, filtering, or acceleration. The mouse features six programmable buttons, an ambidextrous design, and customizable RGB lighting. Its long battery life and low-latency wireless performance make it an ideal choice for serious gamers who require optimal control and precision during competitive gameplay."
#     },
#     {
#         "name": "Bose QuietComfort 35 II Wireless Bluetooth Headphones",
#         "id": "Bose QC35 II",
#         "price": 24999,
#         "type": "Accessories",
#         "offers": "5% off with SBI Debit Card, 10% Instant Discount on Credit Cards",
#         "warranty_details": "2 years",
#         "description": "The Bose QuietComfort 35 II headphones are engineered for unparalleled sound and noise-cancellation. Powered by the proprietary Acoustic Noise Cancelling technology, they block out unwanted external noise, allowing for an immersive listening experience. The headphones feature a 40mm driver for clear and balanced audio, with a wide frequency response for deep bass and crisp highs. With a battery life of up to 20 hours, they are perfect for long flights or extended listening sessions. Designed for comfort, they have plush ear cushions and a lightweight frame. Bose’s reputation for audio quality and noise-canceling is reflected in the QC35 II."
#     },
#     {
#         "name": "Mi 11X Pro 5G Smartphone",
#         "id": "Mi 11X Pro 5G",
#         "price": 33999,
#         "type": "Electronics",
#         "offers": "5% off on ICICI Credit Card, 6-month EMI option",
#         "warranty_details": "1 year",
#         "description": "The Mi 11X Pro 5G is a flagship-level smartphone from Xiaomi, offering an impressive set of features at a mid-range price. Powered by the Qualcomm Snapdragon 888 chipset and equipped with an Adreno 660 GPU, it provides seamless performance for gaming, multitasking, and everyday tasks. The 6.67-inch AMOLED display supports a 120Hz refresh rate for smooth scrolling and vivid colors. The 108MP triple-camera setup ensures excellent photography with AI-powered enhancements. With 8GB RAM and 128GB storage, the Mi 11X Pro is a great choice for users who want premium features without the flagship price tag."
#     },
#     {
#         "name": "Sony WH-1000XM4 Noise Cancelling Headphones",
#         "id": "Sony WH-1000XM4",
#         "price": 29990,
#         "type": "Accessories",
#         "offers": "5% Instant Discount with Axis Bank Cards, 10% off on Amazon Pay",
#         "warranty_details": "2 years",
#         "description": "The Sony WH-1000XM4 wireless noise-canceling headphones are regarded as some of the best in the industry. With advanced noise-canceling technology, they create an immersive listening environment, blocking out the sounds of the outside world. The headphones feature a 40mm driver with high-resolution audio support and deliver rich, clear sound across a wide frequency range. They also have a long-lasting battery, providing up to 30 hours of playback. Built with comfort in mind, they have a lightweight design and plush earcups. Sony’s LDAC technology ensures high-quality streaming for audiophiles."
#     },
#     {
#         "name": "Apple MacBook Air (M2, 2023)",
#         "id": "Apple MacBook Air M2",
#         "price": 114999,
#         "type": "Electronics",
#         "offers": "5% off on ICICI Credit Card, EMI available",
#         "warranty_details": "1 year",
#         "description": "The Apple MacBook Air (M2, 2023) is a lightweight, powerful laptop that combines performance with portability. Powered by Apple’s custom M2 chip, which features an 8-core CPU and a 10-core GPU, it offers a significant performance boost over previous models. The 13.6-inch Retina display with True Tone technology ensures vibrant colors and sharp details. With 8GB of RAM and 256GB SSD storage, it provides fast performance for everyday tasks and light creative workloads. Apple’s seamless ecosystem and top-notch build quality make this laptop perfect for professionals, students, and casual users who need a reliable machine for work and play."
#     }
# ]


# additional_products_data = [
#     {
#         "name": "Dell XPS 15 9510 Laptop",
#         "id": "Dell XPS 15 9510",
#         "price": 184999,
#         "type": "Electronics",
#         "offers": "10% off on ICICI Credit Card, Free Shipping",
#         "warranty_details": "2 years",
#         "description": "The Dell XPS 15 9510 is a premium ultrabook known for its powerful performance and sleek design. Powered by the Intel Core i7-11800H processor, it comes with NVIDIA GeForce RTX 3050 Ti graphics, making it ideal for professionals, content creators, and gamers. The 15.6-inch 4K OLED display provides vivid colors and sharp details, enhancing both productivity and entertainment. With 16GB of RAM and a 512GB SSD, it ensures smooth multitasking and fast performance. The XPS 15 is designed for portability and premium quality, perfect for anyone looking for a high-performance laptop."
#     },
#     {
#         "name": "HP Pavilion x360 14-inch Touchscreen Laptop",
#         "id": "HP Pavilion x360",
#         "price": 64999,
#         "type": "Electronics",
#         "offers": "5% off on SBI Credit Card, 10% Instant Discount",
#         "warranty_details": "1 year",
#         "description": "The HP Pavilion x360 is a versatile 2-in-1 laptop that can be used as a laptop or a tablet with its 360-degree hinge. Featuring an Intel Core i5 processor and 8GB of RAM, it delivers solid performance for everyday tasks. The 14-inch Full HD touchscreen display offers clear visuals and easy interaction. The laptop also features 512GB SSD storage for fast access to your files. Whether you’re working or watching movies, the Pavilion x360’s compact design and flexibility make it an excellent choice for those who need portability and functionality."
#     },
#     {
#         "name": "Seagate Expansion 1TB External Hard Drive",
#         "id": "Seagate Expansion 1TB",
#         "price": 3999,
#         "type": "Storage",
#         "offers": "5% off on ICICI Credit Card, Free Shipping",
#         "warranty_details": "1 year",
#         "description": "The Seagate Expansion 1TB External Hard Drive is a reliable and easy-to-use storage solution for all your data needs. With a USB 3.0 interface, it offers high-speed file transfers and is compatible with both Windows and Mac systems. The drive comes pre-formatted for Windows, making it plug-and-play. Whether you need additional space for documents, movies, or photos, the Seagate Expansion Drive provides an easy and affordable way to store and back up your files."
#     },
#     {
#         "name": "Netgear Nighthawk AC2300 Smart WiFi Router",
#         "id": "Netgear Nighthawk AC2300",
#         "price": 8999,
#         "type": "Networking",
#         "offers": "10% off on HDFC Credit Cards, Free Installation",
#         "warranty_details": "2 years",
#         "description": "The Netgear Nighthawk AC2300 is a high-performance Wi-Fi router designed to deliver fast and reliable internet speeds. Equipped with 4 high-performance antennas and a dual-band Wi-Fi design, it offers up to 2300 Mbps of total bandwidth. Ideal for large homes or multiple devices, this router ensures that you get uninterrupted HD streaming, online gaming, and fast internet speeds throughout your home. It also includes advanced security features such as WPA3 encryption and a built-in firewall for added protection."
#     },
#     {
#         "name": "Western Digital My Passport 2TB External Hard Drive",
#         "id": "Western Digital My Passport 2TB",
#         "price": 6299,
#         "type": "Storage",
#         "offers": "5% off on HDFC Debit Cards",
#         "warranty_details": "3 years",
#         "description": "The Western Digital My Passport 2TB External Hard Drive offers ample space for all your documents, photos, videos, and other important files. With a USB 3.0 interface, this portable drive offers fast transfer speeds for quickly moving large files. The My Passport drive is compatible with both Windows and Mac OS and comes with 256-bit AES hardware encryption to secure your data. Its compact design makes it easy to take anywhere, while its durability ensures long-term protection for your files."
#     },
#     {
#         "name": "Asus RT-AC86U AC2900 Dual-Band Wi-Fi Router",
#         "id": "Asus RT-AC86U",
#         "price": 15999,
#         "type": "Networking",
#         "offers": "10% off on ICICI Credit Card",
#         "warranty_details": "2 years",
#         "description": "The Asus RT-AC86U AC2900 is a high-speed Wi-Fi router with advanced features for gamers and power users. With speeds up to 2900 Mbps, it supports both 2.4GHz and 5GHz bands, providing smooth performance for HD streaming, gaming, and large file transfers. It features advanced security with AiProtection powered by Trend Micro and MU-MIMO technology for simultaneous streaming to multiple devices. The router's powerful antennas ensure long-range Wi-Fi coverage, making it ideal for large homes."
#     },
#     {
#         "name": "Logitech G Pro X Wireless Lightspeed Gaming Mouse",
#         "id": "Logitech G Pro X Wireless",
#         "price": 11999,
#         "type": "Accessories",
#         "offers": "10% off with ICICI Credit Card",
#         "warranty_details": "2 years",
#         "description": "The Logitech G Pro X Wireless Lightspeed Gaming Mouse is designed for competitive gamers seeking precision and performance. It features Logitech’s exclusive HERO 25K sensor with a 25,600 DPI sensitivity, providing pixel-perfect accuracy. The mouse offers ultra-low latency with Lightspeed wireless technology and has a durable, lightweight design with customizable button profiles. The Pro X also includes a detachable cable for wired mode and is equipped with RGB lighting that can be customized via Logitech G Hub software."
#     },
#     {
#         "name": "Samsung 970 EVO Plus 500GB NVMe M.2 SSD",
#         "id": "Samsung 970 EVO Plus 500GB",
#         "price": 6899,
#         "type": "Storage",
#         "offers": "5% off on HDFC Debit Card",
#         "warranty_details": "5 years",
#         "description": "The Samsung 970 EVO Plus is a high-performance NVMe M.2 SSD designed for both gaming and professional workloads. With read speeds up to 3500MB/s and write speeds up to 3300MB/s, it offers exceptional performance for tasks such as video editing, gaming, and large file transfers. The 500GB capacity provides ample storage space for games and applications, while the advanced heat management ensures consistent performance during heavy use. The SSD comes with Samsung’s Magician software for easy performance monitoring and data management."
#     },
#     {
#         "name": "Lenovo Legion 5i 15.6-inch Gaming Laptop",
#         "id": "Lenovo Legion 5i",
#         "price": 129999,
#         "type": "Electronics",
#         "offers": "10% off with Axis Bank Credit Card, Free Shipping",
#         "warranty_details": "1 year",
#         "description": "The Lenovo Legion 5i is a high-performance gaming laptop designed for the ultimate gaming experience. It features the latest Intel Core i7-10750H processor and an NVIDIA GeForce GTX 1660 Ti GPU for smooth graphics and fast performance. The 15.6-inch Full HD display offers a 144Hz refresh rate for fluid visuals, while the 16GB RAM and 512GB SSD ensure seamless multitasking and fast boot-up times. The Legion 5i also features advanced cooling technology to keep the laptop cool during long gaming sessions."
#     },
#     {
#         "name": "TP-Link Deco M4 AC1200 Whole Home Mesh WiFi System",
#         "id": "TP-Link Deco M4",
#         "price": 6999,
#         "type": "Networking",
#         "offers": "5% off on SBI Debit Card",
#         "warranty_details": "2 years",
#         "description": "The TP-Link Deco M4 is a Whole Home Mesh Wi-Fi System that provides seamless Wi-Fi coverage for large homes. With a dual-band AC1200 design, it delivers speeds up to 1200 Mbps, ensuring fast and reliable internet for all your devices. The system includes two units that can cover up to 4000 square feet and is compatible with Alexa for voice control. The Deco M4 is easy to set up using the Deco app and includes advanced security features like WPA3 encryption to protect your network."
#     },
#     {
#         "name": "Sony WH-1000XM4 Wireless Noise Cancelling Headphones",
#         "id": "Sony WH-1000XM4",
#         "price": 29999,
#         "type": "Accessories",
#         "offers": "5% off with ICICI Credit Card",
#         "warranty_details": "1 year",
#         "description": "The Sony WH-1000XM4 are premium wireless noise-canceling headphones that deliver exceptional sound quality and a comfortable fit. Equipped with advanced noise-canceling technology, they block out ambient noise, allowing you to focus on your music or work. The headphones feature a long battery life of up to 30 hours, quick charging, and a touch-sensitive control panel. With a stylish design and support for high-resolution audio, the WH-1000XM4 is ideal for audiophiles and frequent travelers."
#     },
#     {
#         "name": "Samsung Odyssey G7 27-inch Curved Gaming Monitor",
#         "id": "Samsung Odyssey G7",
#         "price": 38999,
#         "type": "Electronics",
#         "offers": "10% off on HDFC Credit Card, EMI options available",
#         "warranty_details": "1 year",
#         "description": "The Samsung Odyssey G7 27-inch Curved Gaming Monitor offers an immersive gaming experience with its 1000R curve and a fast 240Hz refresh rate. Featuring a 2560x1440p resolution and support for both NVIDIA G-Sync and AMD FreeSync Premium Pro, it provides smooth visuals with no screen tearing. The QLED display ensures vibrant and accurate colors, making it perfect for competitive gamers. The monitor’s sleek design and adjustable stand add to its appeal, while its superior performance makes it an excellent choice for both casual and professional gamers."
#     }
# ]



# products_collection.insert_many(additional_products_data)








