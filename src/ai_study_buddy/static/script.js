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
        'results.title.summary': 'Your Summary',
        'results.title.quiz': 'Your Quiz',
        'results.title.flashcards': 'Your Flashcards'
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
        'results.title.summary': 'Твоето обобщение',
        'results.title.quiz': 'Твоят тест',
        'results.title.flashcards': 'Твоите флашкарти'
    }
}

// Buttons
const fileInputBtn = document.getElementById('file-input')
const removeFileBtn = document.querySelector('.remove-file')
const generateBtn = document.getElementById('generate-button')

let selectedFile = null
let selectedGenerator = 'summary'


function main() {
    applyLanguage(DEFAULT_LANGUAGE)

    document.querySelectorAll('.lang-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            applyLanguage(btn.dataset.lang)
        })
    })

    document.getElementById('upload-area').addEventListener('click', () => {
        fileInputBtn.click()
    })

    fileInputBtn.addEventListener('change', (e) => {
        selectedFile = e.target.files[0]

        if (selectedFile){
            document.querySelector('.selected-file').style.display = 'flex'
            document.getElementById('file-icon').textContent = selectedFile.name.split('.').pop().toLowerCase()
            document.getElementById('file-name').textContent = selectedFile.name
        }
    })

    removeFileBtn.addEventListener('click', () => {
        selectedFile = null
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

}


async function generateService() {
    const formData = new FormData()
    formData.append('file', selectedFile)

    const response = await fetch(`http://127.0.0.1:8000/generate/${selectedGenerator}`, {
        method: 'POST',
        body: formData
    })

    const data = await response.json()

    console.log(data['summary'])

    document.querySelector('.result').style.display = 'block'
    updateTranslation(document.querySelector('.result-title'), `results.title.${selectedGenerator}`)
    updateTranslation(document.querySelector('.result-type'), `generation.${selectedGenerator}`)
}


function applyLanguage(lang) {
    document.documentElement.lang = lang
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.dataset.i18n
        el.textContent = translations[lang][key]
    })

    // Active status on language button
    document.querySelectorAll('.lang-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.lang === lang)
    })
}


function updateTranslation(element, key) {
    const currentLang = document.documentElement.lang
    element.dataset.i18n = key
    element.textContent = translations[currentLang][key]
}