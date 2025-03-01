##


## Multi-agent solution
The best approach for our project is to build a system with several smart parts working together. Using a multi-agent approach brings a lot of benefits.  We'll have a main computer server that acts like a brain, and lots of smaller devices out in the world that act like eyes, spotting potholes. They will all talk to each other and share what they see. Each agent, whether it’s a piece of software or a device, is really good at its job and works with the others to achieve our big goal: detecting potholes quickly and accurately. This way, we can quickly find out where the potholes are and fix them. It's like creating a team of experts, each with their own job, but all working towards the same goal of making our roads better and safer. Here's how it works in simple terms:
-	FastAPI: This is like our project's coordinator. It's super fast and can handle lots of requests from the agents without getting tired. It talks to our databases, like SQLite, and SPARQL knowledge bases, to get or/and store information.
-	Databases and Knowledge Bases: SQLite keeps our data organized and ready to use. The SPARQL knowledge base is like a smart library that helps us find specific information when we need it. In our implementation, when starting the server, we download the main KPIs from the knowledge base and store them along with the rest of the parameters in the config.json file.
-	Pre-trained YOLOv8 Models: These are our experts in recognizing what a pothole looks like in different situations. They've learned from lots of pictures and can now spot potholes quickly.
-	Telegram Bot with AIOGram: This is like a remote control for our project based on common Docker local network with FastAPI with fast communication. We can use it to change settings or check on things without having to be at the computer all the time.
-	Confidence, Skyline, Mode Settings: These settings let us adjust how picky our pothole detector is and to select settings for a specific configuration of equipment on the agent for detecting potholes on the roads . We can make it more or less strict depending on what we need, or how the equipment is installed (for example, the angle of the surveillance camera), etc.
-	User Access and Server Choices: We can decide who gets to use our system and which server should do the work. If one server is busy, we could have a backup ready.


###

