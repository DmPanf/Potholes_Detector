### A high-level architecture diagram

![image](https://github.com/DmPanf/Potholes_Detector/assets/99917230/1558b991-b4ca-431b-a1f3-505c9e08c910)

The image depicts a high-level architecture diagram of a system that integrates various technologies, including FastAPI, Docker, and a Telegram bot.

In simple terms, FastAPI is a modern, fast (high-performance) web framework for building APIs with Python. It's based on standard Python type hints, which helps you create robust and production-ready APIs. In this architecture, FastAPI is used to create an interface for CRUD operations (Create, Read, Update, Delete) which can be accessed via HTTP methods (POST, GET, PUT, DELETE). These operations are likely to interact with databases and potentially other services like a knowledge base or rule base.

The diagram includes a Telegram bot, which suggests that the system can be controlled and interacted with through Telegram. Bots are automated Telegram accounts programmed to handle messages or commands and can be used to integrate with other systems or services.

Docker is a containerization platform that packages applications and their dependencies together in a container to ensure that they work seamlessly in any environment. In this context, it appears that FastAPI and the Telegram bot are running inside Docker containers on the same Docker host. This means they are isolated from the operating system but can communicate with each other through defined network settings.

The diagram also shows Swagger UI, which is a tool used to document and test APIs. It provides a web-based user interface that allows developers and users to interact with the API and understand its capabilities without reading through code or definitions.

The overall architecture is designed to work on a server, with components such as databases and potentially machine learning models like YOLO (You Only Look Once, which is a real-time object detection system) integrated into the system.

Here's a breakdown of how FastAPI might work with a Telegram Bot in one Docker environment:

- FastAPI provides the backend API with endpoints that the Telegram bot can interact with.
- The Telegram bot receives commands from users and sends requests to the FastAPI endpoints.
- FastAPI processes these requests, interacts with databases or other services as needed, and sends back the responses.
- The Telegram bot receives the responses and delivers the results to the user in the Telegram app.

This setup allows users to interact with a complex system through the familiar interface of a Telegram bot, simplifying tasks such as data retrieval, system configuration, or even controlling and monitoring machine learning models and processes.

### Telegram Bot

The user interface of a Telegram bot typically involves chat interactions where users can send messages, commands, or queries, and receive responses. When a user inputs data incorrectly, the bot is programmed to recognize these errors and provide feedback. This feedback usually includes an error message explaining what went wrong and suggestions for how to input the correct data.

For example, if a user is supposed to enter a date in a specific format (like YYYY-MM-DD) and they enter it incorrectly, the bot might respond with a message such as, "The date format is incorrect. Please enter the date in the 'YYYY-MM-DD' format." This helps guide users towards successful interactions with the bot.


### Training Results

### The Confusion Matrix

![image](https://github.com/DmPanf/Potholes_Detector/assets/99917230/982c87ab-a1df-4bff-8e9c-b2d94c4a3438)

The confusion matrix in the image represents the performance of the YOLOv8 model on one of the training datasets for pothole detection.

- **True Positives (Top Left Square)**: The model correctly identified 248 instances as potholes. These are the true positives, indicating cases where the model's prediction and the actual label agree that the potholes are present.

- **False Negatives (Bottom Left Square)**: There are 2 instances where the model incorrectly predicted the background (no pothole) when there was actually a pothole. These are false negatives, which suggest that the model missed detecting potholes in these cases.

- **True Negatives (Bottom Right Square)**: This cell of the matrix is not explicitly labeled, but it implies the number of true negatives, where the model correctly identified there were no potholes, and there were indeed none. Since it's not labeled, we assume it might have a high number consistent with a well-performing model, but the exact value is not visible.

- **False Positives (Top Right Square)**: There are 10 instances where the model incorrectly identified potholes when none were present. These are false positives, representing over-detection by the model.

In conclusion, the YOLOv8 model appears to be performing quite well on this dataset, with a high number of true positives and relatively low numbers of false negatives and false positives. However, the true negative count is missing from the confusion matrix, which is essential for a complete understanding of the model's performance, particularly its specificity. The high number of true positives and low number of false negatives and positives suggests that the model is effective at detecting potholes with a high degree of precision and recall.

Based on the provided confusion matrix data, the following quality metrics for the YOLOv8 model training on the pothole detection dataset are calculated:

- **Precision**: Approximately 96.12%, indicating a high accuracy of the model in classifying an image as containing a pothole when it does.

- **Recall**: About 99.2%, showing that the model is highly capable of identifying most of the positive pothole cases in the dataset.

- **F1 Score**: Approximately 97.64%, which is a balanced measure that takes into account both the precision and the recall. This high F1 score suggests that the model has a harmonious balance of precision and recall, making it very effective in the pothole detection task.


<code>
# Given values from the confusion matrix
true_positives = 248
false_negatives = 2
false_positives = 10
# True negatives are not provided, but they are not needed for precision, recall, and F1 score calculations.

# Precision calculation (the ability of the classifier not to label as positive a sample that is negative)
precision = true_positives / (true_positives + false_positives)

# Recall calculation (the ability of the classifier to find all the positive samples)
recall = true_positives / (true_positives + false_negatives)

# F1 Score calculation (the harmonic mean of precision and recall)
f1_score = 2 * (precision * recall) / (precision + recall)

precision, recall, f1_score

</code>
![image](https://github.com/DmPanf/Potholes_Detector/assets/99917230/419f19b0-7a9e-49e8-96f8-693d1f540004)


The image depicts a series of plots showing various metrics and loss values over the course of training a YOLOv8 model, likely for the task of object detection such as pothole identification on roads.

- **Box Loss (Train and Validation)**: These plots show the loss associated with the bounding box predictions. Both training and validation box losses decrease steadily over time, which indicates that the model is getting better at accurately predicting the location and size of the bounding boxes around the potholes.

- **Class Loss (Train and Validation)**: The classification loss represents the model's ability to correctly classify the objects within the bounding boxes. Both plots show a sharp decline and then level off, suggesting that the model quickly learned to classify the objects correctly and then made incremental improvements.

- **Objectness Loss (Train and Validation)**: This is depicted as "train/obj_loss" and "val/obj_loss" (though labeled as 'df1_loss' in the plots, which might be a specific notation for the dataset or framework used). These plots show the loss related to the confidence of the object presence within the bounding box. The trend is similar to the box and class losses, with a decrease over epochs indicating improving confidence in predictions.

- **Precision and Recall**: These metrics are crucial for understanding the model's performance. The precision plot shows that the model is consistently accurate in its predictions, and the recall plot indicates that the model is able to identify most of the relevant objects. Both metrics appear to have reached a high level, which suggests that the model has a good balance between precision and recall.

- **mAP (Mean Average Precision) at IOU=50 and IOU=50-95**: The mAP at IOU=50 is near perfect, which suggests that the model is very accurate when the Intersection Over Union (IOU) threshold is at 50%. The mAP at IOU thresholds between 50% and 95% shows a gradual increase, which suggests the model performs well across a range of strictness in overlap criteria, although it's less accurate at the highest thresholds.

Overall, the plots indicate that the model has trained effectively, with loss metrics showing improvement and performance metrics indicating high precision and recall. The mAP scores suggest that the model is quite robust, performing well across different IOU thresholds. This suggests that the model would likely perform well in practical applications, such as detecting potholes in various conditions.

---

### The objective function

The objective function described here is specifically designed to evaluate the performance of a model tasked with pothole detection. This function plays a central role in the model's training process, as it quantifies the model's accuracy in classifying potholes. The primary goal during training is to minimize this function, which, in essence, means reducing the number of errors the model makes in pothole prediction.

The objective function is defined as:

\[ E(N_{ep}, \text{datasets}, \text{augmentation}, I_r, N_{pic}) = N_{cor} - N_{incor} \rightarrow \min \]

Where the components of the function are:

- **E**: This represents the pothole classification error. It's a measure of how well the model is performing, with a lower value indicating better performance.

- **Ncor (Correctly Detected Potholes)**: This is the number of potholes that the model has correctly identified. A higher count of correctly detected potholes contributes positively to model performance.

- **Nincor (Missed Potholes)**: This counts the potholes that the model failed to detect. The goal is to minimize this number, as each missed pothole is a classification error.

- **Nep (Number of Epochs)**: This refers to the number of complete passes through the training dataset. The number of epochs can affect the model’s learning and its eventual performance.

- **Ir (Image Resolution)**: The resolution of images used in training can significantly impact the model's ability to detect potholes accurately. Different resolutions may be experimented with to find the optimal setting for the model.

- **Datasets**: These are collections of images used for training, encompassing various weather conditions like dry, rainy, snowy, etc. The diversity in the datasets ensures that the model is robust and can perform well under different real-world conditions.

- **Augmentation**: This is the process of artificially expanding the training dataset by altering the images, such as by rotating, cropping, changing brightness, etc. Augmentation helps in making the model more generalizable and less prone to overfitting.

- **Npic (Number of Elements in the Training Set)**: This is the total number of images or elements in the training dataset. A larger dataset can provide more comprehensive training, but it also requires more computational resources.

By focusing on minimizing this objective function, the training process aims to enhance the model's ability to accurately detect potholes while reducing the likelihood of missing any. This optimization leads to a more reliable and effective pothole detection model.
