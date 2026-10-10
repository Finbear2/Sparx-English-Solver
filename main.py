from playwright.sync_api import sync_playwright
from random import randint
from jev import ask, init
import re

targetWPM = 334

with sync_playwright() as p:

    context = p.firefox.launch_persistent_context(
        "browser-profile",
        headless=False
    )
    page = context.pages[0] if context.pages else context.new_page()

    while True:
        page.goto('https://reader.sparx-learning.com/library')

        page.wait_for_timeout(15000)
        title = page.title()
        if title != 'Home - Sparx Reader':
            input('Press enter when logged in...')

        print('\nPressing first button...')
        button = page.get_by_role(
            "button",
            name=re.compile(r"(Start|Continue) your current task")
        )
        button.click()

        print('Pressed! Pressing next button...')
        button = page.get_by_role(
            "button",
            name=re.compile(r"(Start|Continue) Reading")
        )
        button.click()
        print('Pressed!')

        page.wait_for_timeout(5000)
        paragraphs = page.locator(".read-content p").all_inner_texts()
        text = ' '.join(paragraphs)
        words = text.split()
        print('Amount of words:', len(words))
        wpm = randint(targetWPM-30, targetWPM+30)
        time = (len(words)/targetWPM) * 60000

        print('\nWaiting for ', time/1000, 'seconds')
        page.wait_for_timeout(time)
        init()

        page.get_by_role("button", name="I have read up to here").click()

        for i in range(4):
            page.wait_for_timeout(3000)
            question = page.locator(
                ".PanelPaperbackQuestionContainer h2").inner_text()

            answers = page.locator(
                ".PanelPaperbackQuestionContainer button[type='button']"
            ).all_inner_texts()

            options = []

            for answer in answers:
                issues = ['Not in story', ' Scroll for more...']
                if not answer in issues:
                    options.append(answer)

            print("\nQuestion:", question)
            print("Answers:", options)
            correct = ask(text, words, question, options)
            print('\nCorrect Answer:', correct)

            page.get_by_role("button", name=correct).click()
            page.get_by_role("button", name='Continue').click()
    input('>>> ')
