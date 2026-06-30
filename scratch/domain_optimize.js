const fs=require('fs');

// === 1. lib/data.ts — hero title/description → domain-driven, not tech-driven ===
let data=fs.readFileSync('E:/Coding/LeoPortfolio/src/lib/data.ts','utf8');

data=data.replace(
  "Full-stack engineer — Android, backend, IoT, and applied AI.",
  "I build systems that have to work — and keep working."
);
data=data.replace(
  "I spent a decade shipping software under real constraints: factory floors with no signal, messaging for thousands of users, devices that run 24/7 without updates, and AI that actually deploys. Not demos. Production.",
  "Over the past decade, I've designed and delivered systems across manufacturing, enterprise communications, energy management, and AI research — environments where reliability, domain understanding, and the ability to bridge hardware and software matter more than any single technology stack."
);
fs.writeFileSync('E:/Coding/LeoPortfolio/src/lib/data.ts',data);
console.log('1. data.ts done');

// === 2. app/layout.tsx — SEO metadata ===
let layout=fs.readFileSync('E:/Coding/LeoPortfolio/src/app/layout.tsx','utf8');
layout=layout.replace(
  "Leo Zhang — Full-stack Engineer | Android · Backend · IoT · AI",
  "Leo Zhang — Systems Engineer | Smart Manufacturing · Enterprise Communications · Applied AI"
);
layout=layout.replace(
  "Full-stack engineer with 10+ years shipping Android, backend, IoT, and AI systems. Factory floors to research labs — I build things that work. Based in Auckland, NZ.",
  "Systems engineer with 10+ years delivering reliable software for manufacturing, enterprise messaging, energy management, and AI research. Based in Auckland, NZ."
);
layout=layout.replace(
  '"Full-stack Engineer | Android · Backend · IoT · AI"',
  '"Systems Engineer | Smart Manufacturing · Enterprise Communications · Applied AI"'
);
fs.writeFileSync('E:/Coding/LeoPortfolio/src/app/layout.tsx',layout);
console.log('2. layout.tsx done');

// === 3. home/about-section.tsx — about prose → domain storytelling ===
let about=fs.readFileSync('E:/Coding/LeoPortfolio/src/components/home/about-section.tsx','utf8');

about=about.replace(
  /<p className="mt-6 text-lg text-muted-foreground leading-relaxed">[\s\S]*?<\/p>\s*<p className="mt-4 text-muted-foreground leading-relaxed">[\s\S]*?<\/p>\s*<p className="mt-4 text-muted-foreground leading-relaxed">[\s\S]*?<\/p>/,
`<p className="mt-6 text-lg text-muted-foreground leading-relaxed">
            My first real project was a live-streaming chat-room platform for a
            small IoT start-up. Over the next ten years, I followed the company's
            evolution into smart manufacturing, enterprise communications, and
            energy management — designing, building, and maintaining systems that
            had to keep running no matter what.
          </p>
          <p className="mt-4 text-muted-foreground leading-relaxed">
            I led the smart factory platform from a single-site pilot to five
            production sites serving hundreds of workers daily. I shipped an
            enterprise IM system that ran at sub-200ms latency with under 2%
            downtime for a decade. I built an offline-first GIS app for forest
            rangers working in zero-signal zones, and a smart power monitoring
            platform that saved 15% energy across multiple parks. Each project
            taught me the same lesson: the hardest part of engineering isn't
            the code — it's understanding the environment it has to survive in.
          </p>
          <p className="mt-4 text-muted-foreground leading-relaxed">
            Most recently, I completed a Master's at AUT in Auckland with First
            Class Honours, where I built a multimodal AI virtual try-on system
            that published at IVCNZ 2025. I'm looking for a team that values
            engineering judgment, domain learning, and the ability to deliver
            systems that work under real constraints — whatever the stack.
          </p>`
);
fs.writeFileSync('E:/Coding/LeoPortfolio/src/components/home/about-section.tsx',about);
console.log('3. about-section.tsx done');

// === 4. home/about-section.tsx — highlights → domain-focused ===
about=fs.readFileSync('E:/Coding/LeoPortfolio/src/components/home/about-section.tsx','utf8');
about=about.replace(
  /const highlights: HighlightItem\[\] = \[[\s\S]*?\];/,
`const highlights: HighlightItem[] = [
  {
    counter: { value: 21, suffix: "" },
    label: "systems delivered — across manufacturing, communications, energy, field operations, and AI",
    color: "text-blue-500",
    bgColor: "bg-blue-500",
  },
  {
    counter: { value: 10, suffix: "+" },
    label: "years of production delivery — from start-up phase through growth and pivot",
    color: "text-purple-500",
    bgColor: "bg-purple-500",
  },
  {
    counter: { value: 5, suffix: "+" },
    label: "factory sites — smart manufacturing serving hundreds of workers daily",
    color: "text-green-500",
    bgColor: "bg-green-500",
  },
  {
    counter: { value: 5000, formatFn: (n: number) => n.toLocaleString() },
    label: "daily active users — enterprise messaging, sub-200ms latency, <2% downtime over 10 years",
    color: "text-orange-500",
    bgColor: "bg-orange-500",
  },
  {
    counter: { value: 1, suffix: "st", prefix: "" },
    label: "Class Honours — Master's at AUT, multimodal AI research, published at IVCNZ 2025",
    color: "text-pink-500",
    bgColor: "bg-pink-500",
  },
];`
);
fs.writeFileSync('E:/Coding/LeoPortfolio/src/components/home/about-section.tsx',about);
console.log('3b. highlights updated');

// === 5. app/projects/page.tsx — hero description ===
let projects=fs.readFileSync('E:/Coding/LeoPortfolio/src/app/projects/page.tsx','utf8');
projects=projects.replace(
  '21 projects across a decade of production delivery — factory automation, enterprise messaging, IoT, mobile GIS, live streaming, and applied AI.',
  '21 projects across a decade of production delivery. Each one solved a specific problem under real constraints — unreliable networks, factory-floor hardware, zero-signal forests, and high-security environments.'
);
fs.writeFileSync('E:/Coding/LeoPortfolio/src/app/projects/page.tsx',projects);
console.log('5. projects/page.tsx done');

// === 6. app/research/page.tsx — intro description ===
let research=fs.readFileSync('E:/Coding/LeoPortfolio/src/app/research/page.tsx','utf8');
research=research.replace(
  'a decade building and shipping systems across six engineering domains.',
  'a decade of shipping reliable systems under real-world constraints, and the reflection that comes after.'
);
fs.writeFileSync('E:/Coding/LeoPortfolio/src/app/research/page.tsx',research);
console.log('6. research/page.tsx done');

console.log('\nAll 6 files domain-optimized!');
