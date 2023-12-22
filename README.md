## Pothole Detector Project
Road maintenance is a critical aspect of urban management, directly influencing safety and comfort for all traffic participants. One of the common issues that plague drivers, cyclists, and even pedestrians are potholes. Potholes can cause accidents, damage vehicles, and even impede emergency services. Addressing this issue promptly is essential for a safe and efficient transportation system. 


The goal is straightforward and quantifiable: to develop a multi-agents system capable of detecting potholes in real time with a high degree of accuracy and with a sufficiently high processing speed, marking detected potholes as dangerous or relatively safe by their width in the image. This system should be capable of being deployed in a vehicle or roadside monitoring equipment to identify and report the location of potholes to a central database. 


To achieve this goal, we need to accomplish several tasks: 

1. Collect and curate a dataset of road images that include various pothole conditions. 

2. Train the YOLOv8 model to recognize and accurately pinpoint potholes in these images. 

3. Develop a FastAPI backend capable of receiving image data from the detection system, processing it, and updating the central database in real-time. 

4. Carry out the necessary testing to ensure that the system is reliable and can work under different lighting and weather conditions. 

5. Show the ability to manage the system via Telegram bot and serve various clients such as other bots, web applications or simple clients connected to the server through a single API.

   
![image](https://github.com/DmPanf/Potholes_Detector/assets/99917230/eba33da8-a4b6-45ce-993d-751e8e355af3)


Using a multi-agent system for pothole detection is smart because: 
- **It's Faster**: Many scouts can check different areas at the same time. 

- **It's Scalable**: You can start with a few scouts and add more as you need them. 

- **It's Flexible**: Scouts can be on different vehicles and use different routes every day. 

- **It's Robust**: If one agent fails, the others will still be able to do their job. 

- **It's Efficient**: The manager can organize the information and make sure it's used well. 

By fulfilling these tasks, we aim to create a tool that not only improves road conditions but also enhances public safety and potentially saves on long-term road maintenance costs.  

In each case, these agents work independently but contribute to a central system that collects, analyzes, and responds to the data on potholes, which helps the city fix roads faster and more efficiently. This can lead to safer driving, fewer accidents, and happy citizens.

---

## Use Cases
Here's how and where we could use a multi-agent system for detecting potholes: 

- **In City Buses**: They travel all around the city every day. Each bus can have a camera that sends pictures to the server when it sees a pothole. 

- **In Taxi Fleets**: Taxis can have an app that lets drivers report potholes with a button click, and the location is sent to the server. 

- **With Delivery Drones**: As drones fly overhead, they can take pictures and report back potholes from a bird's eye view. 

- **On Garbage Trucks**: They cover nearly every street once a week, making them great for scouting potholes. 

- **By Common People**: Ordinary people can install a simple application on their phones. If they notice a pothole, they can take a picture, and it will immediately go to the server with the geolocation of the place and with all the necessary details in a single database. 

- **By Various equipment of Road Services**: Vehicles and road maintenance equipment such as wipers and snow plows or dedicated drones can be equipped with cameras and sensors. As they drive through the city to perform their usual maintenance tasks, they can simultaneously detect potholes and report them. This integration improves the efficiency of road services by combining maintenance with pothole detection. 

- **By Google Glasses**: People wearing Google Glasses or similar augmented reality devices can contribute to pothole detection and be instantly alerted to potential hazards. When a pit is detected, the glasses can automatically capture an image and send it to the server. This method is especially effective in low-light conditions, as glasses can improve visibility, making it easier to detect potholes and report them at night or in poorly lit places, saving people from possible injury. 

- **Future Integration in Modern Cars**: Looking ahead, modern cars equipped with advanced sensors and cameras can be utilized for pothole detection. These vehicles, especially those with features like heads-up displays, can project signs and information about the road surface, including potholes, directly onto the driver's windshield. This not only contributes to the pothole detection database but also immediately informs drivers about potential road hazards, enhancing safety.

---

## Main Components of FastAPI: 

- **Pydantic for Data Handling**: It's used for data validation and settings management, which simplifies parsing and validating JSON data. 

- **Path Operations**: FastAPI uses path operations like GET, POST, PUT, and DELETE, which are essential for building APIs. 

- **Dependency Injection System**: FastAPI has a powerful, but easy-to-use dependency injection system. It allows you to have reusable dependencies that you can inject into your route functions. 

- **Starlette for the Web Layer**: This handles all the web interactions - routes, requests, and responses. It's what allows FastAPI to be a fully-functional web framework. 

- **Background Tasks**: FastAPI allows you to run functions in the background. This is useful for operations that need to happen after returning a response. 

- **WebSockets Support**: FastAPI also supports WebSockets, which allows for real-time communication between the client and the server. 

- **Testing**: FastAPI provides easy testing with Pytest, making it simple to check the behavior of your applications. 

- **Swagger UI**: Swagger UI is a great tool for anyone developing or using an API. It's like an instruction manual and control panel for your API, all in one. 

![image](https://github.com/DmPanf/Potholes_Detector/assets/99917230/331ee411-b62a-479f-8eb8-c829d09a35be)


## Conclusion 

When reflecting on a project like the Pothole Detection using YOLOv8 and FastAPI, it's important to consider both the successes and challenges, as well as the insights gained and future plans.  

### Successful Implementations 

- **Effective Pothole Detection**: We successfully integrated the YOLOv8 model, enabling accurate and efficient detection of potholes in various road conditions. This was a key achievement, as it forms the core of our project's functionality. 

- **User-Friendly Interface**: The creation of an intuitive interface through a Telegram bot and a web application was another significant success. These platforms allow users to easily interact with our system, upload images or videos, and receive processed results. 

- **Real-Time Processing and Feedback**: Implementing FastAPI for real-time image processing and immediate feedback was a crucial aspect we managed to achieve. This ensures that the system operates efficiently and responds quickly to user requests. 

---

### Challenges and Unsuccessful Attempts 

- **Handling Varied Lighting and Weather Conditions**: One of the problems we faced was the inconsistency of the model's characteristics under different lighting and weather conditions. Achieving consistent accuracy in all scenarios remains a work in progress and requires more careful selection of the dataset and image labeling. 

- **Scalability Issues**: As our user base has grown, we have encountered some scalability issues, especially when processing simultaneous requests for large images and videos, which we intend to eliminate in future updates. At the very beginning, we mentioned that the project provides for scaling and load balancing on multiple servers with an increase in the number of requests. 

 

### Insights Gained 

- **Importance of Data Quality**: The learning curve was steep regarding data quality and diversity. The effectiveness of the model hinges significantly on these factors, shaping our approach towards future data collection and model training processes. Through training YOLOv8 on various datasets, we discovered the profound impact of data quality, quantity, and the balance between different types of objects. Focusing on the single class of 'potholes', we observed that the model's ability to detect typical or specific types of potholes varied based on the dataset composition. For example, skewing the dataset towards images of wet or snow-covered roads altered the model's detection capabilities, clearly demonstrating how the weights in the model training are influenced. We also realized the importance of avoiding unnatural augmentations, such as 180-degree flipped images of vehicles or road surfaces, which can detrimentally affect the model's learning process. The more precise and balanced the image selection and annotation are, the higher the quality of the results and the confidence level of the detections. 

- **Importance of API in Progressive Development**: The project underscored the significance of using APIs for phased designing and incremental functionality additions, especially after the system becomes operational. In the initial stages, the server could be accessed using simple methods like command-line tools (e.g., curl), basic Python scripts in Google Colab or an IDE, and even through Swagger UI without writing a single line of code. This flexibility proved highly advantageous for team collaboration, system debugging, and developing the client-side of the application.  

- **User-Centric Design**: User feedback illuminated the crucial role of a user-friendly interface and the necessity for results to be easily comprehensible. This insight has profoundly influenced our design approach and feature implementations, ensuring that the system is not only efficient but also accessible and intuitive for users.

### Future Plans and Developments 

- **Enhancing Model Robustness**: We plan to retrain the model with a more diverse dataset, including images under various environmental conditions, to improve its accuracy and reliability. There is also an idea to use various trained models on highly specialized datasets - in winter with priority on snow-covered roads, in rainy weather. weather with priority on wet asphalt and puddle pits, and we also plan to consider the option of night roads in poor lighting. 

- **Scaling the System**: To address scalability, we aim to optimize our server infrastructure and explore more efficient data processing techniques. One of the possible options may be effective in sending a short video to the processing model instead of a single image to pre-select a frame with better characteristics and clarity. 

- **Expanding Functionality**: Future developments include adding additional features to the bot, such as custom alerts when serious potholes are detected, and integration with mapping services for better geographical tracking of road conditions. It is also planned to use additional sensors to measure the depth of potholes on roads.

In summary, while we have achieved key milestones in pothole detection and user interaction, we acknowledge the challenges faced, particularly in model consistency and system scalability. The insights gained from this project are invaluable and will significantly shape our future endeavors to enhance the system's effectiveness and expand its capabilities.

![image](https://github.com/DmPanf/Potholes_Detector/assets/99917230/39758834-a657-43bc-925c-0248186a80d6)


## Links

- https://github.com/tensorflow/models/tree/master/research/object_detection?ref=gilberttanner.com
- https://ml.i-neti.ru/map-mean-average-precision/
- 
