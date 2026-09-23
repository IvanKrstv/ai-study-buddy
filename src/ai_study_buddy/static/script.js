document.addEventListener('DOMContentLoaded', main)

// Default language
const DEFAULT_LANGUAGE = 'en'

// Language translations in EN and BG
const translations = {
    'en': {
        'header.title': 'Study smarter, not harder.',
        'header.paragraph': 'Upload your study material and turn it into a summary, quiz, or set of flashcards.',
        'upload.instructions': 'Upload your study notes',
        'upload.drop_file': 'Drop your file here',
        'upload.choose_file': 'or choose a file from your device',
        'upload.browse': 'Browse files',
        'upload.file_types': 'PDF, DOCX or TXT. Maximum 10 MB',
        'selected_file': 'Selected file',
        'selected_file.generation': 'Ready to generate',
        'generation.question': 'What would you like to generate?',
        'generation.summary': 'Summary',
        'generation.summary_text': 'Get the key concepts and important information in a concise format.',
        'generation.quiz': 'Quiz',
        'generation.quiz_text': 'Test your understanding with questions based on your material.',
        'generation.flashcards': 'Flashcards',
        'generation.flashcards_text': 'Turn important concepts into quick study cards.',
        'generate': 'Generate',
        'results.title.summary': 'Summary',
        'results.title.quiz': 'Quiz',
        'results.title.flashcards': 'Flashcards',
        'quiz.next': 'Next Question',
        'quiz.finish': 'See Results',
        'quiz.complete': 'Quiz Complete!',
        'quiz.retry': 'Try Again',
        'quiz.correct': 'Correct',
        'quiz.incorrect': 'Incorrect',
        'quiz.question_of': 'Question {current} of {total}',
        'quiz.score_message_great': 'Excellent work! You have a strong understanding of the material.',
        'quiz.score_message_good': 'Good job! Review the topics you missed to strengthen your knowledge.',
        'quiz.score_message_needs_work': 'Keep studying! Review the material and try again.',
        'flashcard.card_of': 'Card {current} of {total}',
        'flashcard.question': 'Question',
        'flashcard.answer': 'Answer',
        'flashcard.hint': 'Click the card to flip it',
        'flashcard.prev': 'Previous',
        'flashcard.next': 'Next',
        'generate.loading': 'Generating…',
        'generate.error': 'Something went wrong. Please try again.'
    },

    'bg': {
        'header.title': 'Учи ефикасно.',
        'header.paragraph': 'Качи учебния си материал и го превърни в обобщение, тест или флашкарти.',
        'upload.instructions': 'Качи бележките си',
        'upload.drop_file': 'Пусни файла тук',
        'upload.choose_file': 'или избери файл от устройството си',
        'upload.browse': 'Разгледай файлове',
        'upload.file_types': 'PDF, DOCX или TXT. Максимум 10 MB',
        'selected_file': 'Избран файл',
        'selected_file.generation': 'Готов за генериране',
        'generation.question': 'Какво искаш да генерираш?',
        'generation.summary': 'Обобщение',
        'generation.summary_text': 'Виж ключовите концепции и най-важната информация в сбит формат.',
        'generation.quiz': 'Тест',
        'generation.quiz_text': 'Тествай наученото с въпроси, базирани на материала ти.',
        'generation.flashcards': 'Флашкарти',
        'generation.flashcards_text': 'Превърни важните концепции в бързи учебни флашкарти.',
        'generate': 'Генерирай',
        'results.title.summary': 'Обобщение',
        'results.title.quiz': 'Тест',
        'results.title.flashcards': 'Флашкарти',
        'quiz.next': 'Следващ въпрос',
        'quiz.finish': 'Виж резултатите',
        'quiz.complete': 'Тестът е завършен!',
        'quiz.retry': 'Опитай отново',
        'quiz.correct': 'Правилно',
        'quiz.incorrect': 'Грешно',
        'quiz.question_of': 'Въпрос {current} от {total}',
        'quiz.score_message_great': 'Отлична работа! Имаш добро разбиране на материала.',
        'quiz.score_message_good': 'Добра работа! Прегледай темите, които си пропуснал, за да затвърдиш знанията си.',
        'quiz.score_message_needs_work': 'Продължавай да учиш! Прегледай материала и опитай отново.',
        'flashcard.card_of': 'Карта {current} от {total}',
        'flashcard.question': 'Въпрос',
        'flashcard.answer': 'Отговор',
        'flashcard.hint': 'Кликни върху картата, за да я обърнеш',
        'flashcard.prev': 'Предишна',
        'flashcard.next': 'Следваща',
        'generate.loading': 'Генериране…',
        'generate.error': 'Нещо се обърка. Моля, опитай отново.'
    }
}

// Buttons
const fileInputBtn = document.getElementById('file-input')
const removeFileBtn = document.querySelector('.remove-file')
const generateBtn = document.getElementById('generate-button')

let selectedFile = null
let selectedGenerator = 'summary'

// Quiz
let quizData = null
let currentQuestionIndex = 0
let quizScore = 0
let answered = false

// Flashcards
let flashcardData = null
let currentCardIndex = 0


function main() {
    applyLanguage(DEFAULT_LANGUAGE)
    document.querySelectorAll('.lang-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            applyLanguage(btn.dataset.lang)
        })
    })

    const uploadArea = document.getElementById('upload-area')

    uploadArea.addEventListener('click', () => {
        fileInputBtn.click()
    })

    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault()
        uploadArea.classList.add('dragover')
    })

    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('dragover')
    })

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault()
        uploadArea.classList.remove('dragover')
        if (e.dataTransfer && e.dataTransfer.files.length > 0) {
            handleFileSelection(e.dataTransfer.files[0])
        }
    })

    fileInputBtn.addEventListener('change', (e) => {
        if (e.target.files && e.target.files.length > 0) {
            handleFileSelection(e.target.files[0])
        }
    })

    removeFileBtn.addEventListener('click', () => {
        selectedFile = null
        fileInputBtn.value = ''
        document.querySelector('.selected-file').style.display = 'none'
    })

    document.querySelectorAll('.option').forEach(el => {
        el.addEventListener('click', (e) => {
            document.querySelectorAll('.option').forEach(el => {
                el.classList.remove('active')
            })
            e.currentTarget.classList.toggle('active')
            selectedGenerator = e.currentTarget.id
        })
    })
    generateBtn.addEventListener('click', generateService)

    document.getElementById('quiz-next-btn').addEventListener('click', nextQuestion)
    document.getElementById('quiz-retry-btn').addEventListener('click', retryQuiz)

    document.getElementById('flashcard-container').addEventListener('click', flipCard)
    document.getElementById('flashcard-prev-btn').addEventListener('click', prevFlashcard)
    document.getElementById('flashcard-next-btn').addEventListener('click', nextFlashcard)
}


function handleFileSelection(file) {
    if (!file) return
    selectedFile = file
    document.querySelector('.selected-file').style.display = 'flex'
    document.getElementById('file-icon').textContent = file.name.split('.').pop().toUpperCase()
    document.getElementById('file-name').textContent = file.name
}


async function generateService() {
    const previousPEl = document.querySelector('.study-card p')
    if (previousPEl) {
        previousPEl.remove()
    }

    if (!selectedFile) {
        const pEl = document.createElement('p')
        pEl.textContent = 'Please select a file with your notes...'
        document.querySelector('.study-card').appendChild(pEl)

        return
    }

    const currentLang = document.documentElement.lang

    generateBtn.disabled = true
    generateBtn.textContent = translations[currentLang]['generate.loading']

    try {
        const formData = new FormData()
        formData.append('file', selectedFile)

        const response = await fetch(`http://127.0.0.1:8000/generate/${selectedGenerator}`, {
            method: 'POST',
            body: formData
        })

        if (!response.ok) {
            const error = await response.json().catch(() => null)
            alert(error?.detail || translations[currentLang]['generate.error'])
            return
        }

        const data = await response.json()

        document.getElementById('result-section').style.display = 'none'
        document.getElementById('quiz-section').style.display = 'none'
        document.getElementById('quiz-score-section').style.display = 'none'
        document.getElementById('flashcard-section').style.display = 'none'

        switch (selectedGenerator) {
            case 'summary':
                getSummary(data)
                break
            case 'quiz':
                getQuiz(data)
                break
            case 'flashcards':
                getFlashcards(data)
                break
        }
    } catch (error) {
        if (error.message !== 'Not such state') {
            alert(translations[currentLang]['generate.error'])
        }
    } finally {
        generateBtn.disabled = false
        generateBtn.textContent = translations[currentLang]['generate']
    }
}


function getSummary(data) {
    document.getElementById('result-section').style.display = 'block'
    updateTranslation(document.querySelector('.result-title'), `results.title.${selectedGenerator}`)

    const resultContent = document.querySelector('.result-content p')
    resultContent.textContent = data['summary'] ? data['summary'].trim() : ''
}


function getQuiz(data) {
    quizData = data['quiz']['questions']
    currentQuestionIndex = 0
    quizScore = 0
    startQuiz()
}


function getFlashcards(data) {
    flashcardData = data['flashcards']['flashcards']
    currentCardIndex = 0
    startFlashcards()
}


// Quiz functions
function startQuiz() {
    document.getElementById('quiz-section').style.display = 'block'
    renderQuestion()
}


function renderQuestion() {
    const currentLang = document.documentElement.lang
    const question = quizData[currentQuestionIndex]
    const total = quizData.length
    answered = false

    // Update progress text
    const progressText = translations[currentLang]['quiz.question_of']
        .replace('{current}', currentQuestionIndex + 1)
        .replace('{total}', total)
    document.getElementById('quiz-progress').textContent = progressText

    // Progress bar
    const progressPercent = ((currentQuestionIndex) / total) * 100
    document.getElementById('quiz-progress-fill').style.width = `${progressPercent}%`

    document.getElementById('quiz-question-text').textContent = question.question

    const optionsContainer = document.getElementById('quiz-options')
    optionsContainer.innerHTML = ''

    const letters = ['A', 'B', 'C', 'D', 'E', 'F']

    question.options.forEach((option, index) => {
        const optionEl = document.createElement('div')
        optionEl.className = 'quiz-option'

        const letterEl = document.createElement('div')
        letterEl.className = 'quiz-option-letter'
        letterEl.textContent = letters[index]

        const textEl = document.createElement('div')
        textEl.className = 'quiz-option-text'
        textEl.textContent = option

        optionEl.appendChild(letterEl)
        optionEl.appendChild(textEl)
        optionEl.addEventListener('click', () => selectAnswer(index))
        optionsContainer.appendChild(optionEl)
    })

    document.getElementById('quiz-explanation').style.display = 'none'
    document.getElementById('quiz-explanation').className = 'quiz-explanation'
    document.querySelector('.quiz-nav').style.display = 'none'
}


function selectAnswer(selectedIndex) {
    if (answered) return
    answered = true

    const question = quizData[currentQuestionIndex]
    const correctIndex = question.correct_answer_index
    const isCorrect = selectedIndex === correctIndex

    if (isCorrect) quizScore++

    const options = document.querySelectorAll('.quiz-option')
    options.forEach((option, index) => {
        option.classList.add('disabled')

        if (index === correctIndex) {
            option.classList.add('correct')
        } else if (index === selectedIndex && !isCorrect) {
            option.classList.add('incorrect')
        }
    })

    // Show explanation
    const explanationEl = document.getElementById('quiz-explanation')
    explanationEl.style.display = 'flex'
    explanationEl.classList.add(isCorrect ? 'correct-explanation' : 'incorrect-explanation')

    document.getElementById('quiz-explanation-icon').textContent = isCorrect ? '✓' : '✗'
    updateTranslation(document.getElementById('quiz-explanation-title'), isCorrect ? 'quiz.correct' : 'quiz.incorrect')
    document.getElementById('quiz-explanation-text').textContent = question.explanation

    // Show nav button
    const navEl = document.querySelector('.quiz-nav')
    navEl.style.display = 'block'

    const nextBtn = document.getElementById('quiz-next-btn')
    const isLast = currentQuestionIndex === quizData.length - 1

    updateTranslation(nextBtn, isLast ? 'quiz.finish' : 'quiz.next')
}


function nextQuestion() {
    currentQuestionIndex++

    if (currentQuestionIndex >= quizData.length) {
        showScore()
    } else {
        renderQuestion()
    }
}


function showScore() {
    const total = quizData.length
    const percent = Math.round((quizScore / total) * 100)

    // Show score
    document.getElementById('quiz-section').style.display = 'none'
    document.getElementById('quiz-score-section').style.display = 'block'

    document.getElementById('quiz-score-value').textContent = `${quizScore} / ${total}`

    let messageKey
    if (percent >= 80) {
        messageKey = 'quiz.score_message_great'
    } else if (percent >= 50) {
        messageKey = 'quiz.score_message_good'
    } else {
        messageKey = 'quiz.score_message_needs_work'
    }

    updateTranslation(document.getElementById('quiz-score-message'), messageKey)
}


function retryQuiz() {
    currentQuestionIndex = 0
    quizScore = 0

    document.getElementById('quiz-score-section').style.display = 'none'
    document.getElementById('quiz-section').style.display = 'block'

    renderQuestion()
}


// Flashcard functions
function startFlashcards() {
    document.getElementById('flashcard-section').style.display = 'block'
    renderFlashcard()
}


function renderFlashcard() {
    const currentLang = document.documentElement.lang
    const card = flashcardData[currentCardIndex]
    const total = flashcardData.length

    document.getElementById('flashcard').classList.remove('flipped')

    const progressText = translations[currentLang]['flashcard.card_of']
        .replace('{current}', currentCardIndex + 1)
        .replace('{total}', total)
    document.getElementById('flashcard-progress').textContent = progressText

    // Progress bar
    const progressPercent = ((currentCardIndex + 1) / total) * 100
    document.getElementById('flashcard-progress-fill').style.width = `${progressPercent}%`

    document.getElementById('flashcard-front-text').textContent = card.question
    document.getElementById('flashcard-back-text').textContent = card.answer

    document.getElementById('flashcard-prev-btn').disabled = currentCardIndex === 0
    document.getElementById('flashcard-next-btn').disabled = currentCardIndex === total - 1
}


function flipCard() {
    document.getElementById('flashcard').classList.toggle('flipped')
}


function prevFlashcard() {
    if (currentCardIndex > 0) {
        currentCardIndex--
        renderFlashcard()
    }
}


function nextFlashcard() {
    if (currentCardIndex < flashcardData.length - 1) {
        currentCardIndex++
        renderFlashcard()
    }
}


// Language functions
function applyLanguage(lang) {
    document.documentElement.lang = lang
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.dataset.i18n
        el.textContent = translations[lang][key]
    })

    // Active language
    document.querySelectorAll('.lang-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.lang === lang)
    })

    // Re-render quiz progress if quiz is active
    if (quizData && document.getElementById('quiz-section').style.display === 'block') {
        const progressText = translations[lang]['quiz.question_of']
            .replace('{current}', currentQuestionIndex + 1)
            .replace('{total}', quizData.length)
        document.getElementById('quiz-progress').textContent = progressText
    }

    // Re-render flashcard progress if flashcards are active
    if (flashcardData && document.getElementById('flashcard-section').style.display === 'block') {
        const progressText = translations[lang]['flashcard.card_of']
            .replace('{current}', currentCardIndex + 1)
            .replace('{total}', flashcardData.length)
        document.getElementById('flashcard-progress').textContent = progressText
    }
}


function updateTranslation(element, key) {
    if (!element) return
    const currentLang = document.documentElement.lang
    element.dataset.i18n = key
    element.textContent = translations[currentLang]?.[key] || ''
}