const workshopDetails = [
    {
        title: "A Rusteacean Introduction to Shellcoding",
        description: `During this enjoyable afternoon workshop, you will learn how to implement your next shellcode or implant using the Rust programming language.

 

The workshop will cover the following:

- A brief introduction to Rust.
- Key challenges during shellcode development and how to resolve them.
- A brief introduction to Windows and parsing PE headers.
- Creation of fully position-independent code (PIC), similar to Cobalt Strike Beacon.
- Implementation of at least one common technique for bypassing AV/EDR.`,
        leftContent: [
            "Presenter:",
            "Ben Stuart",
            "Capacity:",
            "10",
            "Language of the workshops:",
            "English",
            "Location:",
            "Artic Wolf, Messeturm, 19th Floor,  Friedrich-Ebert-Anlage 49, You WILL need ID or a passport to enter the workshop area.",
            "Start", "08:45",
            "End", "12:45"
        ],
        rightContent: [
            "Duration:",
            "4h",
            "Requirements:",
            `You will need to bring a Windows VM to the workshop. This VM should have X64dbg (64-bit) installed.
You will also need the ability to transfer files from and to it. A development container (Docker) for cross-compiling Rust will be provided.`,
            "Audience level:",
            "intermediate"
        ],
        registrationLink: "https://registrationwillopensoon.local/register/workshop1" 
    },
    {
        title: "Automated Purple Teaming - where offense meets defense with fine-grained CTI",
        description: `In this hands-on session, we'll focus on the practical side of automated adversary emulation to get the most benefit for our cyber defense.

 

Key Topics:
- fundamentals of purple team
- getting familiar with atomic red team
- learn to create detection rules within Elasticsearch
- building workflows to automate your testing and evaluation`,
        leftContent: [
            "Presenter:",
            "Marcus Gruber",
            "Capacity:",
            "10",
            "Language of the workshops:",
            "English",
            "Location:",
            "Artic Wolf, Messeturm, 19th Floor,  Friedrich-Ebert-Anlage 49, You WILL need ID or a passport to enter the workshop area.",
            "Start", "14:15",
            "End", "18:15"
        ],
        rightContent: [
            "Duration:",
            "4h",
            "Requirements:",
            `you will need a Windows VM and Docker/Podman on your system or separate VM. You WILL need ID or a passport to enter the workshop area!`,
            "Audience level:",
            "intermediate"
        ],
        registrationLink: "https://registrationwillopensoon.local/register/workshop2" 
    },
    {
        title: "Forensics Workshop - An introduction to forensic artifacts on Windows systems and tools to analyze them.",
        description: "Filesystem Artifacts and Evidence of Execution on Windows Systems. A description of the artifacts and the tools to analyze them, with a subsequent guided analysis",
        leftContent: [
            "Presenter:",
            "Felix Rother",
            "Capacity:",
            "10",
            "Language of the workshops:",
            "English",
            "Location:",
            "Office SECUINFRA GmbH, Münchener Str. 36, 60329 Frankfurt am Main",
            "Start", "14:15",
            "End", "18:15"
        ],
        rightContent: [
            "Duration:",
            "4h",
            "Requirements:",
            "You only need a laptop with internet access and an RDP client. The internet access will be provided through our guest Wi-Fi in Frankfurt.",
            "Audience level:",
            "beginner - intermediate"
        ],
        registrationLink: "https://registrationwillopensoon.local/register/workshop3" 
    },
    {
        title: "Challenges when automating Agentic AI Red Teaming",
        description: "Intro to Agentic AI Red Teaming and AI Transparency, Hands-on demo of tooling (agentic-radar and some others) that help automate Agentic AI Red Teaming, what is required for remediation and compliance reporting.",
        leftContent: [
            "Presenter:",
            "Ante Gojsalic",
            "Capacity:",
            "20",
            "Language of the workshops:",
            "English",
            "Location:",
            "Siemens Energy, Hahnstr. 43e, 60528 Frankfurt am Main - You WILL need ID or a passport to enter the workshop area!",
            "Start", "14:15",
            "End", "18:15"
        ],
        rightContent: [
            "Duration:",
            "4h",
            "Requirements:",
            "just a laptop with internet access, no special software required. You WILL need ID or a passport to enter the workshop area!",
            "Audience level:",
            "beginner"
        ],
        registrationLink: "https://registrationwillopensoon.local/register/workshop4" 
    },

    {
        title: "Exploring Defender for Endpoint response features, endpoint logs, and some KQL",
        description: "This session covers the features of Defender for Endpoint, which analysts might benefit from during investigations and IR. We'll also review the log data MDE provides to analysts and interesting detection use cases. Attendees will access a test tenant to write and execute KQL queries.",
        leftContent: [
            "Presenter:",
            "Ethan Bowen",
            "Capacity:",
            "20",
            "Language of the workshops:",
            "English",
            "Location:",
            "NVISO Office FFM, Holzgraben 5, 60313 Frankfurt am Main",
            "Start", "14:15",
            "End", "18:15"
        ],
        rightContent: [
            "Duration:",
            "4h",
            "Requirements:",
            "just a laptop",
            "Audience level:",
            "beginner - intermediate"
        ],
        registrationLink: "https://registrationwillopensoon.local/register/workshop5" 
    },

    {
        title: "Introduction to Physical Security Testing",
        description: "Join us for an interactive half-day workshop where you'll learn the essential techniques of physical security testing. This session covers key skills such as lock picking, door bypass methods, and cloning insecure access cards. Gain hands-on experience as you practice these techniques and hear real-world access attempts from experienced Red Teamers. Enhance your understanding of physical security measures and test your newfound skills on our Cover Access Vault (CAV).",
        leftContent: [
            "Presenter:",
            "Nico Leidecker / Harris Nuhanovic",
            "Capacity:",
            "10",
            "Language of the workshops:",
            "English",
            "Location:",
            "NVISO Office FFM, Holzgraben 5, 60313 Frankfurt am Main",
            "Start", "08:45",
            "End", "12:45"
        ],
        rightContent: [
            "Duration:",
            "3-4h",
            "Requirements:",
            "just good mood and a willingness to learn",
            "Audience level:",
            "beginner"
        ],
        registrationLink: "https://registrationwillopensoon.local/register/workshop5" 
    },

    {
        title: "Bank Under Siege: Red and Blue Team Tactics",
        description: `This workshop offers an immersive cybersecurity experience through a gamified scenario focused on financial institutions. Participants will be divided into Red and Blue Teams. The game board simulates a financial environment, where the Red Team aims to compromise systems, while the Blue Team defends them.
The session begins with an interactive setup phase, where the Red Team selects tactics to achieve their objectives, and the Blue Team focuses on understanding the environment and choosing initial defenses. The core of the workshop involves a game loop, with teams alternating between planning and executing actions. The Red Team explores attack vectors like breached credentials or malware deployment, while the Blue Team implements countermeasures such as enhanced network monitoring or access controls.

The workshop concludes with a recap session, summarizing key learnings and discussing outcomes. This interactive approach enhances participants' understanding of cybersecurity dynamics, focusing on both offensive and defensive strategies. Attendees will improve teamwork and communication skills, learning to prioritize actions during critical situations and gaining insights into strategic approaches fundamental to Red and Blue Team operations.`,
        leftContent: [
            "Presenter:",
            "tbd",
            "Capacity:",
            "20",
            "Language of the workshops:",
            "English",
            "Location:",
            "NVISO Office FFM, Holzgraben 5, 60313 Frankfurt am Main",
            "Start", "08:45",
            "End", "12:45"
        ],
        rightContent: [
            "Duration:",
            "4h",
            "Requirements:",
            "No requirements",
            "Audience level:",
            "beginner"
        ],
        registrationLink: "https://registrationwillopensoon.local/register/workshop5" 
    },

    {
        title: "Treasure Hunt - A Beginner's Voyage into Pentesting",
        description: `Set sail on a hands-on journey into the basics of penetration testing and join the hunt for flags. You will learn how to wield powerful tools like Nmap to chart unknown waters - err, networks -, plunder badly guarded ports, uncover hidden treasures within vulnerable systems and use the right grappling hooks to exploit web applications. Whether you're seeking to understand the fundamentals or gain first-hand experience in pentesting techniques, this workshop is your compass for navigating the essentials of network and application security testing.`,
        leftContent: [
            "Presenter:",
            "Claudia Kutter",
            "Capacity:",
            "20",
            "Language of the workshops:",
            "English",
            "Location:",
            "NVISO Office FFM, Holzgraben 5, 60313 Frankfurt am Main",
            "Start", "08:45",
            "End", "12:45"
        ],
        rightContent: [
            "Duration:",
            "4h",
            "Requirements:",
            "Laptop, Hypervisor (VirtualBox 🪟, UTM 🍏)",
            "Audience level:",
            "beginner"
        ],
        registrationLink: "https://registrationwillopensoon.local/register/workshop5" 
    },

    {
        title: "The Hitchhacker's Guide to the Mobile Galaxy",
        description: `Grab your towel and embark on a journey through the intricacies of the Android operating system. Uncover the secrets and vulnerabilities of mobile apps through static analysis. Ignite the infinite improbability drive and delve deeper with dynamic analysis to gain the skills and knowledge to outwit the Vogons. In this workshop, not only the Ultimate Question of Life, the Universe, and Everything will be answered but also most of your questions regarding Android application security.`,
        leftContent: [
            "Presenter:",
            "Claudia Kutter",
            "Capacity:",
            "20",
            "Language of the workshops:",
            "English",
            "Location:",
            "NVISO Office FFM, Holzgraben 5, 60313 Frankfurt am Main",
            "Start", "14:15",
            "End", "18:15"
        ],
        rightContent: [
            "Duration:",
            "4h",
            "Requirements:",
            "Laptop, Android Studio",
            "Audience level:",
            "beginner"
        ],
        registrationLink: "https://registrationwillopensoon.local/register/workshop5" 
    }
    
];