// src/JS/modules/prediction.js
/**
 * Career Prediction Quiz Module
 */

let currentQuestion = 0;
let quizStarted = false;
let answers = {};

const QUIZ_QUESTIONS = [
    {
        id: 1,
        text: "What aspect of work is most important to you?",
        subtext: "Choose the factor that matters most",
        options: [
            { text: "💰 High salary and financial stability", value: "salary" },
            { text: "🎯 Making an impact and solving problems", value: "impact" },
            { text: "🎨 Creative expression and innovation", value: "creativity" },
            { text: "👥 Working with people and collaboration", value: "people" }
        ]
    },
    {
        id: 2,
        text: "How do you prefer to learn new skills?",
        options: [
            { text: "📚 Formal education and certifications", value: "formal" },
            { text: "💻 Hands-on projects and learning by doing", value: "hands_on" },
            { text: "👨‍🏫 Mentorship and direct guidance", value: "mentorship" },
            { text: "🧪 Experimentation and self-discovery", value: "experimentation" }
        ]
    },
    {
        id: 3,
        text: "What's your ideal work environment?",
        options: [
            { text: "🏢 Large corporate structure with clear hierarchy", value: "corporate" },
            { text: "🚀 Startup with fast-paced innovation", value: "startup" },
            { text: "🤝 Collaborative team with flat structure", value: "collaborative" },
            { text: "🏠 Remote or flexible work arrangement", value: "remote" }
        ]
    },
    {
        id: 4,
        text: "Which skill would you like to develop most?",
        options: [
            { text: "💻 Technical & Programming", value: "technical" },
            { text: "📊 Data & Analytics", value: "analytics" },
            { text: "🎨 Design & User Experience", value: "design" },
            { text: "📢 Communication & Leadership", value: "communication" }
        ]
    },
    {
        id: 5,
        text: "How important is job security to you?",
        options: [
            { text: "🔒 Very important - I need stability", value: "high_security" },
            { text: "⚖️ Somewhat important - balance needed", value: "medium_security" },
            { text: "🎢 Not important - I like risk and challenges", value: "low_security" }
        ]
    },
    {
        id: 6,
        text: "What's your experience level?",
        options: [
            { text: "🎓 Fresh graduate / No professional experience", value: "fresh" },
            { text: "🌱 0-2 years of experience", value: "junior" },
            { text: "📈 2-5 years of experience", value: "mid" },
            { text: "🏆 5+ years of experience", value: "senior" }
        ]
    },
    {
        id: 7,
        text: "Do you prefer working with technology?",
        options: [
            { text: "❤️ Absolutely! Tech is my passion", value: "tech_lover" },
            { text: "👍 Yes, but open to other fields", value: "tech_open" },
            { text: "😐 Neutral - doesn't matter much", value: "neutral" },
            { text: "❌ Not really - prefer non-tech", value: "non_tech" }
        ]
    },
    {
        id: 8,
        text: "What type of problems excite you?",
        options: [
            { text: "🧠 Complex algorithmic challenges", value: "algorithmic" },
            { text: "📈 Business and strategy problems", value: "business" },
            { text: "👨‍👩‍👧‍👦 People and organizational issues", value: "people_problems" },
            { text: "🌍 Social impact and sustainability", value: "social_impact" }
        ]
    }
];

function startQuiz() {
    quizStarted = true;
    answers = {};
    currentQuestion = 0;
    
    document.getElementById('initialState').style.display = 'none';
    document.getElementById('questionCard').style.display = 'block';
    document.getElementById('progressContainer').style.display = 'block';
    document.getElementById('resultsSection').style.display = 'none';
    
    showQuestion();
}

function showQuestion() {
    const q = QUIZ_QUESTIONS[currentQuestion];
    
    // Update progress
    updateProgress();
    
    // Update question text
    document.getElementById('questionText').textContent = q.text;
    if (q.subtext) {
        document.getElementById('questionSubtext').textContent = q.subtext;
    }
    
    // Render options
    const optionsContainer = document.getElementById('optionsContainer');
    optionsContainer.innerHTML = '';
    
    q.options.forEach((option, index) => {
        const label = document.createElement('label');
        label.className = 'flex items-center gap-3 p-4 border border-[#1e2d42] hover:border-teal-400 rounded-xl cursor-pointer transition-all';
        
        const input = document.createElement('input');
        input.type = 'radio';
        input.name = `q${q.id}`;
        input.value = option.value;
        input.className = 'w-5 h-5';
        input.onchange = () => handleAnswer(q.id, option.value);
        
        if (answers[q.id] === option.value) {
            input.checked = true;
        }
        
        const span = document.createElement('span');
        span.textContent = option.text;
        
        label.appendChild(input);
        label.appendChild(span);
        optionsContainer.appendChild(label);
    });
}

function handleAnswer(questionId, value) {
    answers[questionId] = value;
    
    // Move to next question or show results
    if (currentQuestion < QUIZ_QUESTIONS.length - 1) {
        currentQuestion++;
        showQuestion();
    } else {
        showResults();
    }
}

function updateProgress() {
    const progressFill = document.getElementById('progressFill');
    const currentQuestionSpan = document.getElementById('currentQuestion');
    const progressPercent = document.getElementById('progressPercent');
    
    const percent = ((currentQuestion + 1) / QUIZ_QUESTIONS.length) * 100;
    if (progressFill) progressFill.style.width = percent + '%';
    if (currentQuestionSpan) currentQuestionSpan.textContent = `${currentQuestion + 1}`;
    if (progressPercent) progressPercent.textContent = `${Math.round(percent)}%`;
}

function showResults() {
    document.getElementById('questionCard').style.display = 'none';
    document.getElementById('progressContainer').style.display = 'none';
    document.getElementById('resultsSection').style.display = 'block';
    
    // Calculate result based on answers
    const result = calculateResult();
    
    document.getElementById('resultTitle').textContent = result.title;
    document.getElementById('resultDescription').textContent = result.description;
    document.getElementById('resultIcon').textContent = result.icon;
    
    // Show recommended careers
    const careersContainer = document.getElementById('recommendedCareers');
    careersContainer.innerHTML = '';
    
    result.careers.forEach(career => {
        const careerElement = document.createElement('div');
        careerElement.className = 'bg-[#161f30] border border-[#1e2d42] rounded-lg p-4 mb-3';
        careerElement.innerHTML = `
            <h4 class="font-bold text-[#f1ede6] mb-2">${career.title}</h4>
            <p class="text-slate-400">${career.description}</p>
            <div class="mt-3">
                <span class="bg-teal-400/20 text-teal-400 text-xs px-2 py-1 rounded">${career.match}% Match</span>
            </div>
        `;
        careersContainer.appendChild(careerElement);
    });
}

function calculateResult() {
    // Simple scoring system based on answers
    const scores = {
        technical: 0,
        analytical: 0,
        creative: 0,
        managerial: 0,
        social: 0
    };
    
    // Map answers to scores
    Object.keys(answers).forEach(questionId => {
        const value = answers[questionId];
        
        // Question 1: What aspect of work is most important?
        if (questionId === '1') {
            if (value === 'salary') scores.managerial += 2;
            if (value === 'impact') scores.social += 2;
            if (value === 'creativity') scores.creative += 2;
            if (value === 'people') scores.social += 1;
        }
        
        // Question 2: How do you prefer to learn?
        if (questionId === '2') {
            if (value === 'formal') scores.analytical += 1;
            if (value === 'hands_on') scores.technical += 2;
            if (value === 'mentorship') scores.managerial += 1;
            if (value === 'experimentation') scores.creative += 2;
        }
        
        // Question 3: Ideal work environment
        if (questionId === '3') {
            if (value === 'corporate') scores.managerial += 2;
            if (value === 'startup') scores.technical += 1;
            if (value === 'collaborative') scores.social += 2;
            if (value === 'remote') scores.creative += 1;
        }
        
        // Question 4: Skill to develop
        if (questionId === '4') {
            if (value === 'technical') scores.technical += 2;
            if (value === 'analytics') scores.analytical += 2;
            if (value === 'design') scores.creative += 2;
            if (value === 'communication') scores.social += 2;
        }
        
        // Question 5: Job security importance
        if (questionId === '5') {
            if (value === 'high_security') scores.managerial += 2;
            if (value === 'medium_security') scores.analytical += 1;
            if (value === 'low_security') scores.creative += 1;
        }
        
        // Question 6: Experience level
        if (questionId === '6') {
            if (value === 'fresh') scores.creative += 1;
            if (value === 'junior') scores.technical += 1;
            if (value === 'mid') scores.analytical += 1;
            if (value === 'senior') scores.managerial += 2;
        }
        
        // Question 7: Preference for technology
        if (questionId === '7') {
            if (value === 'tech_lover') scores.technical += 2;
            if (value === 'tech_open') scores.technical += 1;
            if (value === 'neutral') scores.analytical += 1;
            if (value === 'non_tech') scores.social += 1;
        }
        
        // Question 8: Type of problems that excite
        if (questionId === '8') {
            if (value === 'algorithmic') scores.technical += 2;
            if (value === 'business') scores.analytical += 2;
            if (value === 'people_problems') scores.managerial += 2;
            if (value === 'social_impact') scores.social += 2;
        }
    });
    
    // Determine primary strength
    let maxScore = 0;
    let primary = 'analytical'; // default
    
    Object.keys(scores).forEach(key => {
        if (scores[key] > maxScore) {
            maxScore = scores[key];
            primary = key;
        }
    });
    
    // Map to result
    const results = {
        technical: {
            title: "المهندس التقني",
            description: "أنت ماهر في حل المشاكل التقنية وبناء الأنظمة. تحب العمل مع الكود والأدوات التقنية لتطوير منتجات مبتكرة.",
            icon: "💻",
            careers: [
                { title: "مطور برامج", description: "تصميم وتطوير تطبيقات وأنظمة برمجية", match: 95 },
                { title: "مهندسdevops", description: "أتمتة عمليات التطوير والنشر والبنية التحتية", match: 88 },
                { title: "مهندس سحابة", description: "تصميم وإدارة البنية التحتية السحابية والخدمات", match: 85 }
            ]
        },
        analytical: {
            title: "المحلل الاستراتيجي",
            description: "أنت ماهر في تحليل البيانات واتخاذ القرارات المستندة إلى الأدلة. تحب حل المشاكل المعقدة من خلال التحليل الدقيق.",
            icon: "📊",
            careers: [
                { title: "محلل بيانات", description: "جمع وتحليل وتفسير البيانات المعقدة لدعم اتخاذ القرار", match: 92 },
                { title: "مستشار استراتيجي", description: "تقديم توصيات استراتيجية لتحسين أداء الأعمال", match: 89 },
                { title: "محلل أعمال", description: "تحليل احتياجات الأعمال وتحويلها إلى متطلبات تقنية", match: 86 }
            ]
        },
        creative: {
            title: "المبدع المبتكر",
            description: "أنت ماهر في التفكير الإبداعي وتوليد الأفكار الجديدة. تحب التعبير عن نفسك من خلال التصميم والابتكار.",
            icon: "🎨",
            careers: [
                { title: "مصمم تجربة مستخدم", description: "تصميم واجهات وتجارب مستخدم جذابة وسهلة الاستخدام", match: 94 },
                { title: "مصمم جرافيك", description: "إنشاء محتوى بصري ونصوص إبداعية للعلامات التجارية", match: 90 },
                { title: "مبتكر منتجات", description: "توليد وتطوير مفاهيم منتجات جديدة ومبتكرة", match: 87 }
            ]
        },
        managerial: {
            title: "القائد الإداري",
            description: "أنت ماهر في قيادة الفرق وإدارة المشاريع. تحب تنظيم العمل وتحقيق الأهداف من خلال التنسيق الفعال.",
            icon: "👥",
            careers: [
                { title: "مدير مشروع", description: "التخطيط والتنفيذ والمتابعة للمشاريع من البداية للنهاية", match: 93 },
                { title: "مدير فريق", description: "قيادة وإدارة فريق عمل لتحقيق أهداف محددة", match: 90 },
                { title: "مدير منتجات", description: "إدارة دورة حياة المنتج من الفكرة إلى الإطلاق والتحسين", match: 88 }
            ]
        },
        social: {
            title: "المؤثر الاجتماعي",
            description: "أنت ماهر في بناء العلاقات وتحقيق التأثير الاجتماعي. تحب العمل مع الناس وحل المشاكل المجتمعية.",
            icon: "🌍",
            careers: [
                { title: "اختصاصي موارد بشرية", description: "إدارة وتطوير المواهب وبناء ثقافة تنظيمية إيجابية", match: 91 },
                { title: "مسؤول مسؤولية اجتماعية", description: "تصميم وتنفيذ مبادرات تأثير اجتماعي واستدامة", match: 88 },
                { title: "مستشار تنموي", description: "تقديم استشارات لتطوير المجتمعات وتحسين الظروف الحياتية", match: 85 }
            ]
        }
    };
    
    return results[primary] || results.analytical;
}

function nextQuestion() {
    // Validate answer is selected
    if (!answers[QUIZ_QUESTIONS[currentQuestion].id]) {
        alert('Please select an answer before continuing');
        return;
    }
    
    if (currentQuestion < QUIZ_QUESTIONS.length - 1) {
        currentQuestion++;
        showQuestion();
    } else {
        showResults();
    }
}

function previousQuestion() {
    if (currentQuestion > 0) {
        currentQuestion--;
        showQuestion();
    }
}

function goToAgent() {
    window.location.href = 'agent.html';
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    // Hide progress and results on load
    document.getElementById('progressContainer').style.display = 'none';
    document.getElementById('questionCard').style.display = 'none';
    document.getElementById('resultsSection').style.display = 'none';
    document.getElementById('initialState').style.display = 'block';
});