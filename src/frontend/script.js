document.addEventListener('DOMContentLoaded', main)


const DEFAULT_LANGUAGE = 'en'

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


function main() {
    applyLanguage(DEFAULT_LANGUAGE)

    document.querySelectorAll('.lang-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            applyLanguage(btn.dataset.lang)
        })
    })
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

