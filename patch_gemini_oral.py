"""Inject Gemini-polished English oral phrasing into behavioral_common_qa.md."""
path = r"E:\Coding\leozhang2056\Interview\core\behavioral_common_qa.md"

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

N = 0

# === 1. oral-01: Replace self-intro with Gemini-polished version ===
old = """> I'm Leo Zhang, a senior software engineer with a decade of experience across backend, mobile, and IoT systems.

> I moved to New Zealand to complete my master's in AI, focusing on practical machine learning.

> Before that, I worked extensively in manufacturing and enterprise solutions.

> I'm now excited to bring this combined experience to create practical, impactful products."""

new = """> I'm a senior full-stack engineer with over ten years of experience architecting and delivering robust systems across backend, mobile, and IoT platforms.

> Two years ago I came to New Zealand to pursue my Master's, specializing in applied AI \u2014 my thesis focused on diffusion models and production-ready machine learning workflows.

> I have a proven ability to lead teams, optimize system performance, and translate complex requirements into scalable, maintainable software.

> I'm now looking for a long-term engineering role in New Zealand where I can contribute this combined background."""

if old in content:
    content = content.replace(old, new)
    N += 1
    print("1. oral-01: REPLACED")
else:
    print("1. oral-01: NOT FOUND")

# Also update Key Points
old_kp = """- **Role**: Senior software engineer, 10+ years experience
- **Core Systems**: Backend, Mobile, IoT systems
- **Recent Move**: New Zealand for Master's in AI, focused on practical machine learning
- **Prior Background**: Manufacturing and enterprise solutions
- **Forward Look**: Combined experience to create practical, impactful products"""

new_kp = """- **Identity**: Senior full-stack engineer, 10+ years
- **Core**: Backend, Mobile, IoT \u2014 architecting and delivering robust systems
- **NZ Chapter**: Moved to NZ for Master's in Applied AI; thesis on diffusion models and ML workflows
- **Abilities**: Lead teams, optimize performance, translate complexity into maintainable software
- **Goal**: Long-term engineering role in New Zealand"""

if old_kp in content:
    content = content.replace(old_kp, new_kp)
    N += 1
    print("1b. oral-01 Key Points: REPLACED")

# === 2. oral-07: Add Gemini-polished CI/CD script ===
old = """- **Lesson**: Improvement isn't just speed \u2014 it's consistency and reducing reliance on memory.

<a id="oral-08"></a>"""

new = """- **Lesson**: Improvement isn't just speed \u2014 it's consistency and reducing reliance on memory.

#### Primary Script (from Gemini practice)
> We moved from manual deployments \u2014 copying builds, syncing files, uploading by hand \u2014 to a standardized CI/CD pipeline using Jenkins and GitLab.
>
> The setup itself took time: configuring repositories, agents, credentials, and getting the first stable pipeline running. But once the flow became reliable, releases became much more predictable.
>
> We piloted it on Smart Factory first, then gradually rolled out to other products so the team wouldn't maintain ten different deployment habits. We also combined it with containerized services, lightweight checklists, and short internal docs so releases depended less on tribal knowledge.
>
> The biggest improvement wasn't just speed \u2014 it was consistency. Releases became easier to repeat, easier to recover, and much less dependent on individual memory.

<a id="oral-08"></a>"""

if old in content:
    content = content.replace(old, new)
    N += 1
    print("2. oral-07: REPLACED")
else:
    print("2. oral-07: NOT FOUND")

# === 3. oral-08: Add Gemini-polished tough feedback script ===
old = """- **Lesson**: Engineering communication matters; write down context that affects future work.

#### Case B (Optional: Many User Voices)"""

new = """- **Lesson**: Engineering communication matters; write down context that affects future work.

#### Primary Script (from Gemini practice)
> My manager pointed out that I kept too much context in my head, and as the team grew, onboarding and maintenance got harder.
>
> I accepted the feedback and started writing lightweight decision notes for technical choices \u2014 not heavy documentation, just enough so someone new could understand why we made certain calls.
>
> I also added onboarding notes for confusing modules, and kept the habit practical: write down what affects future work, skip the obvious.
>
> That led to smoother onboarding, fewer repeated questions, and better maintainability. When production issues came up, someone else could understand and fix them without pulling me in every time.

#### Case B (Optional: Many User Voices)"""

if old in content:
    content = content.replace(old, new)
    N += 1
    print("3. oral-08: REPLACED")
else:
    print("3. oral-08: NOT FOUND")

# === 4. oral-09: Enhance closing line with Gemini's business-logic focus ===
old = """I\u2019ve learned that **good systems are rarely static**. As scale, cost, and operational reality change, the architecture and process have to evolve too."""

new = """I\u2019ve learned that **good systems are rarely static**. As scale, cost, and operational reality change, the architecture and process have to evolve too \u2014 we stopped maintaining undifferentiated infrastructure and focused on the business logic and real product features instead."""

if old in content:
    content = content.replace(old, new)
    N += 1
    print("4. oral-09: REPLACED")
else:
    print("4. oral-09: NOT FOUND")

# === 5. oral-10: Add Gemini-polished "why hire" primary script ===
old = """For example, I've worked on **enterprise messaging** systems with **real\u2011time** challenges, **Smart Factory** platforms with **devices** and **multi\u2011site deployment**, and more recently **AI\u2011focused** systems during my **Master's at AUT**."""

new = """#### Primary Script (from Gemini practice)
> I bring over ten years of production experience across backend, mobile, and IoT. I'm comfortable working across the full stack, from client to deployment to ops.
>
> I've delivered systems where reliability actually matters: smart factories where the shop floor can't wait, enterprise messaging at real user scale.
>
> I recently specialized in applied AI at AUT, so I combine deep engineering with practical machine learning.
>
> I'm based in Auckland with full work rights, and I'm looking for a team where I can contribute strong execution, reliability, and practical problem-solving \u2014 building products that work in production, not just demos.

#### More detail
For example, I've worked on **enterprise messaging** systems with **real\u2011time** challenges, **Smart Factory** platforms with **devices** and **multi\u2011site deployment**, and more recently **AI\u2011focused** systems during my **Master's at AUT**."""

if old in content:
    content = content.replace(old, new)
    N += 1
    print("5. oral-10: REPLACED")
else:
    print("5. oral-10: NOT FOUND")

# === Write ===
if N > 0:
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"\nDONE: {N} replacements written")
else:
    print("\nNo replacements made")
