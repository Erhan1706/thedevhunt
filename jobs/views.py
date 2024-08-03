from django.shortcuts import render

def job_listings(request):
  data = [ {
        "id": 25,
        "title": "Support Engineer",
        "slug": "support-engineer-25",
        "description": "<h2>Support Engineer</h2>\n<p>Kotlin is a modern programming language targeting the Java virtual machine, Android platform, JavaScript, and Native via LLVM. Launched in 2016, the language is rapidly gaining popularity and now has official support in Android platform, Spring Framework 5, vert.x and Gradle.</p>\n<p>The project is based on pragmatic principles: a convenient range of tools (IDE, build tools, etc.), compatibility, code supportability, and easy learning of the language.</p>\n<h3>We are looking for a support engineer who will:</h3>\n<ul>\n<li>Respond to user requests, identify the problems, and provide the users with all the necessary information to resolve their issues.</li>\n<li>Inform developers about reproducible bugs and issues that need to be addressed.</li>\n</ul>\n<h3>About the project:</h3>\n<ul>\n<li>Kotlin is used by developers from all over the world.</li>\n<li>We communicate with users in open channels. For instance, the Kotlin issue tracker is public.</li>\n<li>User communication is in written English. In the office, we speak Russian, sometimes English.</li>\n<li>Bug reports in <a href=\"https://youtrack.jetbrains.com/issues/KT\">YouTrack</a> make up a significant share of all user requests. We also collect user feedback from our corporate blog, a web forum, a public Slack channel, and are planning to expand to other sources in future.</li>\n</ul>\n<h3>Basic qualifications:</h3>\n<ul>\n<li>Ability to process a large number of requests, willingness to listen to users and understand the essence of their demands and difficulties.</li>\n<li>Good command of written technical English.</li>\n<li>Skills in reproducing bugs and the ability to shorten their descriptions.</li>\n<li>Experience with bugtracker.</li>\n<li>Self-discipline, good time-management skills allowing you not to miss out numerous user requests.</li>\n<li>Familiarity with any JVM programming language: Kotlin, Java, Scala, Groovy, etc.</li>\n</ul>\n<h3>Preferred Qualifications:</h3>\n<ul>\n<li>Familiarity with Kotlin-integrated languages, environments, and tools: IntelliJ IDEA, Maven, Gradle, Android, JavaScript.</li>\n</ul>\n",
        "role": # Do not make this array
            "Support Engineer"
        ,
        "technologies": [
            "Java",
            "Kotlin"
        ],
        "location": [
            "Munich, Germany",
            "Prague, Czech Republic",
            "Amsterdam, Netherlands",
            "Berlin, Germany",
            "Cyprus",
            "Serbia",
            "Armenia"
        ],
        "team": [
            "Kotlin"
        ],
        "language": [
            "English"
        ],
        "company": "JetBrains",
        "remote": True
    },
    {
        "id": 115,
        "title": "Software Developer (RubyMine)",
        "slug": "software-developer-rubymine-115",
        "description": "<p>At JetBrains, code is our passion. Ever since we started, we have strived to make the strongest, most effective developer tools on earth.</p>\n<p>RubyMine is a smart Ruby on Rails IDE, launched in 2008 as the first language-specific IDE on the IntelliJ platform. Supporting over 60,000 developers worldwide, RubyMine provides essential tools such as smart code completion, advanced debugging, VCS support, database integration, and AI assistance. Among our customers are Amazon, Oracle, and GitLab. Click <a href=\"https://www.jetbrains.com/company/people/rubymine/\">here</a> to learn more about the RubyMine team.</p>\n<p>We’re looking for a new Software Developer to work on IDE functionality enhancements, external tool integrations, and new features to improve developer productivity and software efficiency.</p>\n<h3><strong>We will be happy to have you on our team if you:</strong></h3>\n<ul>\n<li>Have at least 3 years of experience in Java/Kotlin development.</li>\n<li>Can design and write code that is easy to read and maintain.</li>\n<li>Understand the algorithms behind the code you write.</li>\n<li>Collaborate effectively, even with people with viewpoints different from your own.</li>\n</ul>\n<h3><strong>We’d be especially thrilled if you:</strong></h3>\n<ul>\n<li>Have contributed to open-source projects or have developed projects of your own.</li>\n<li>Are familiar and experienced with Ruby programming languages.</li>\n<li>Are familiar with compiler development and code analysis technologies.</li>\n<li>Have experience with the IntelliJ Platform.</li>\n<li>Have constructive ideas on how to improve RubyMine and make it better.</li>\n</ul>\n<h3><strong>The challenges we tackle:</strong></h3>\n<p>Our developers’ responsibilities can be broken down into two categories:</p>\n<ul>\n<li>Those related to processing big volumes of source code. The IDE must analyze code on the fly, highlight errors, provide autocompletion suggestions, and support other features.</li>\n<li>Those related to generating code, containerizing tools, or integrating the IDE with external tools like version control systems.</li>\n</ul>\n<p>You may improve any of the subsystems or develop new features of your own design.</p>\n",
        "role": "Software Developer",
        "technologies": [
            "Java"
        ],
        "location": [
            "Munich, Germany",
            "Prague, Czech Republic",
            "Amsterdam, Netherlands",
            "Berlin, Germany",
            "Cyprus",
            "Serbia",
            "Armenia"
        ],
        "team": [
            "RubyMine"
        ],
        "language": [
            "English"
        ],
        "company": "JetBrains",
        "remote": True
    }]
  
  context = {"job_list": data}
  return render(request, 'jobs/jobs.html', context)

def opening(request, company, opening):
  return render(request, 'jobs/opening.html')