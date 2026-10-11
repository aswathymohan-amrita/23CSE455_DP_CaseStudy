# Member 4 — supplied prompt records

**Source folder:** `member4/`; source chat supplied at workspace root as `member4.pdf` and copied here as `Member_4_Source_Chat.pdf`.  
**Identity appearing in the individual report:** Niveditha S, AM.EN.U4EAC23063. This is not verified as the official A11 roster.  
**Project described in these prompts:** initially an Angular-based LMS domain exploration, then `pantharev/lms-fiu-fb-client`, distinct from A11's baseline application.

The following four user prompt entries were extracted from the supplied Gemini chat PDF. Text is reproduced from the PDF's selectable text; line wrapping follows PDF extraction. Responses are not included here.

## Prompt 1

<pre>
Online Learning Application using Angular: Case Study Title Design Pattern Analysis in an Angular-Based
    Online Learning Application Part 1 Investigate: • courses • modules • lessons • quizzes • assignments • students •
    instructors • notifications Identify patterns used in the application. Pay particular attention to patterns associated with: •
    component structure • event communication • service management • hierarchical objects • LLM analysis • Dataset I am
    conducting Part 1 of my Design Patterns case study, titled &quot;Design Pattern Analysis in an Angular-Based Online Learning
    Application.&quot; My required domain includes courses, modules, lessons, quizzes, assignments, students, instructors and
    notifications. Identify such applications/platforms .
</pre>

## Prompt 2

<pre>
ok i have decided to go with the apllication the
    pasted text is the raw readme.md file : # Introduction In today’s age of technology, getting an education online via online
    courses has never been easier. However, people from underdeveloped countries are often cut off from accessing these
    courses due to limitations on their internet data. Facebook allows underdeveloped regions to access their application for
    free with no data charges. The purpose of the application we have developed is to provide a **Learning Management
    System** that is accessible entirely through Facebook, allowing students from anywhere in the world to come and take
    online courses with no data charges. # Current System A 3rd version Single Page Application Web-App that is integrated
    into Facebook. To further elaborate, previous developers have created systems in a similar matter. Each time being
    iterated upon by new developers (us included). # Purpose of New System Create a manageable system using the MEAN
    (MySQL, Express, Angular, NodeJS) full-stack which can run on Facebook. The system is a Learning Management System
    which was created for underdeveloped regions to access through Facebook with no data charges. This system will be the
    4th version of the platform. # User Interface ### Landing Page The landing page to LMS-FIU. Entry can be via the
    website&#x27;s URL, or through Facebook&#x27;s built-in web view. Authentication is granted through Facebook Login. !
    [FB_Profile_Name_NavBar](https://user-images.githubusercontent.com/48221791/91758496-1cdfa380-eb9e-11ea-944b-
    d973ba6d27e3.JPG) ### Course Library Entry point to course library. Here, students can search for courses and enroll in
    them. Furthermore, the system lets the student know which courses they are enrolled in, or are pending for enrollment.
    (pending courses require instructor/administrator approval). ![Course-Library-LMSFIU](https://user-
    images.githubusercontent.com/48221791/91757067-c7a29280-eb9b-11ea-8916-ef81b93ec3e1.JPG) ### Course Modules
    (Student Dashboard) This is the entry point to a course. Here, the student can access the content provided by the course.
    The content is added by an instructor who manages the course. ![Course-Modules-LMSFIU](https://user-
    images.githubusercontent.com/48221791/91757244-ff113f00-eb9b-11ea-932f-2407edc371b0.JPG) ### Student
    Dashboard This is the entry point to the student&#x27;s dashboard. Here, courses that the student is enrolled in are displayed.
    The User Interface changes based on the role of the user. Here, the administrator/instructor can create announcements for
    courses and manage them. ![Student-Dashboard-LMSFIU](https://user-
    images.githubusercontent.com/48221791/91757310-194b1d00-eb9c-11ea-979e-047976c32d9e.JPG) ### Admin
    Dashboard Here, admins can create and manage courses, and manage user roles. In this system, there are three roles:
    Admin, Instructor, and Student. Furthermore, the pending enrollments notification signifies that students have applied for
    enrollment and are awaiting for approval to enter the course. The admin is the one who decides the approval of entry. !
    [Admin_Dashboard](https://user-images.githubusercontent.com/48221791/91758689-662ff300-eb9e-11ea-8f85-
    1d0b98d5fbc2.JPG) ### Create Course Form The admins can create courses through this form, and assign an instructor
    to teach it. The instructor can then add content to the course so that students can consume it. ![Create-Course-LMSFIU]
    (https://user-images.githubusercontent.com/48221791/91757276-0c2e2e00-eb9c-11ea-932f-fc51e6f4f6f1.JPG) # For
    developers The application was generated using Angular CLI version 8.x, which was then updated to Angular and CLI
    version 9.x. To run, utilize the Angular CLI commands and npm commands of npm install -&gt; ng serve once the application
    has been cloned to your computer. Identify the actual frontend framework, Angular version, backend technologies,
    database and major dependencies from repository evidence. Identify the available modules, components, services,
    models, interfaces, routing structure and backend integration. Map the required learning-management features to the
    actual implementation. Clearly distinguish implemented features, partially implemented features, missing features and
    features that cannot be verified. Identify the repository&#x27;s README, dependency configuration, entry points and relevant
    source directories. Assess whether the project is manageable for design-pattern discovery, three subsequent changes,
    UML diagrams and cross-language implementation. Recommend a precise scope of files to inspect and explain what
    should be excluded. Provide a table with the feature, evidence or source path, implementation status and relevance to my
    assignment.
</pre>

## Prompt 3

<pre>
the next part is Identifying and verifying the design patterns : Please examine the actual source code and
    help me identify the design patterns used in the application. Focus on components, communication between components,
    services, dependency injection, course hierarchy, authentication, assessments and notifications. For each pattern you find,
    explain : The pattern name and what it does. Where it is used and which classes or components are involved. The source
    file and line numbers. How the code shows that the pattern is being used. Whether the pattern is confirmed, uncertain or
    not present. Also check for patterns such as Observer, Strategy, Factory, Adapter, Facade, Singleton and Composite, but
    do not assume they are present without evidence.lastly provide : A table summarizing the identified patterns. Detailed
    explanations of the confirmed patterns. A list of patterns that could not be confirmed and why. A simple architecture
    diagram showing how the main components and services interact. A checklist of what I should verify in the source code.
</pre>

## Prompt 4

<pre>
I’m starting Part 2 of my design patterns case study. Using the original code and findings from Part 1, help
    me plan three changes: Add a new assessment type. Change the course hierarchy and support multiple instructor roles.
    Improve the notification system. Explain what needs to change, which design patterns may be affected, and how to test the
    changes. Keep it simple and use the actual code. Don’t modify anything yet
</pre>

The member folder also contains the report/evidence package, which correctly marks implementation-level claims as unverified where source files were unavailable. These prompts and findings concern the LMS-FIU project and are not A11 source evidence.
