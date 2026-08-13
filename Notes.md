When I make an edit:

Push to github, and then
quarto publish gh-pages


Live site is:
https://stevenbogaerts.github.io/etf-info/












## Importing Questions from Canvas

<!--
The Canvas import tool is kept in the [main PrairieLearn GitHub repo](https://github.com/PrairieLearn/PrairieLearn/tree/master/contrib/question_converters/canvas), not to be confused with your own _course_ PrairieLearn repo.
-->

There is a tool for converting questions from Canvas into PrairieLearn. The tool operates on one Canvas quiz at a time. There is no web interface for this tool. Rather, it requires use of your PrairieLearn GitHub repo, so be certain you've followed the steps in the [PrairieLearn GitHub Repository Interface](#repo) section above.

Next, please note the following from the [official Canvas conversion tool documentation](https://github.com/PrairieLearn/PrairieLearn/tree/master/contrib/question_converters/canvas):

> The script will connect to the Canvas API to retrieve the quiz settings and all its questions.
>
> The script currently supports the following question types in Canvas classic quizzes, replacing them with equivalent PrairieLearn elements: essay (tagged as Manual grading), fill-in the blank (including multiple blanks), multiple choice (including true/false and multiple answers), multiple dropdowns, matching, numerical answers and formula (calculated) questions. File upload questions are not currently supported. Text-only "questions" are converted to regular PrairieLearn questions, but you are strongly encouraged to review their use to ensure some gradable component is available.
>
> The script also supports question groups, in which case each question version is saved in a different PrairieLearn question. Given some limitations of the Canvas API, this script does not support question groups linked to question banks. If using question groups, the questions must be included in the Canvas quiz itself instead of in the bank only.
>
> The PrairieLearn assessment will be created with a short name based on the quiz title on Canvas. For each question in the quiz, a new PrairieLearn question is created. Given that question titles are typically unreliable on Canvas, each question will be printed on the terminal, asking for a question title. This title will also be used as a basis to create the QID of the question. If a question should be skipped, just keep the title blank.
>
> While every effort has been made to create the question as close as possible to the original question on Canvas, minor differences may exist, and questions may be able to be optimized for the PrairieLearn environment. For example, this script does not organize the questions into zones, and does not populate question-specific tags to questions. You are strongly encouraged to revise the questions after converting them.

Follow the steps below to use this tool. If you've never work with Python scripts before, then this process may feel a little technical. Please feel free to reach out to me (the ETF faculty advisor) if you have trouble.

<!--
### Get the Canvas Course ID

Go to your main Canvas page. It should be a URL like `https://umich.instructure.com/courses/numbers_here`. The numbers at the end of that URL is your ***Canvas course ID***. Copy that number and save it in a temporary file for now, so that you can access it later.
-->

#### Setting Up config.json

The tool requires a special file to tell it how to access Canvas. Let's create that file. In the root folder of your PrairieLearn repo (the one called `PL-UMICH-<course_name>`), create a new file called `config.json`. Open that file in VS Code and paste the following into it:

```json
{
  "api_url": "https://umich.instructure.com/api/v1",
  "access_token": "YOUR CANVAS ACCESS TOKEN HERE"
}
```

Next, we need to replace the `YOUR CANVAS ACCESS TOKEN HERE` text with a _Canvas access token_. To get one, follow these steps:

- Log in to Canvas.
- Click on your account icon in the top-left corner, then click "Settings".
- Scroll down to the "Approved Integrations" section and click "New Access Token".
- Give it a name (e.g., "PrairieLearn Import") and set an expiration date.

::: {.callout-tip}
Assuming you'll only be using this token for a short period of time, you can set the expiration date to a few days from now. Once your import from Canvas is complete, you won't need the access token anymore.
:::

- Click "Generate Token".
- Copy the generated token into your `config.json` file at the specified place. Make sure you put it inside the quotes. For example, if the token is `12345`, then `config.json` should look like the following:
    ```json
    {
    "api_url": "https://umich.instructure.com/api/v1",
    "access_token": "12345"
    }
    ```
- Click the "X" to close the pop-up window that shows your token. (Don't hit the "Regenerate Token" button, as that will invalidate the token you just generated.)

::: {.callout-warning}
Treat the generated token with the same security you would a password! It allows access to your entire Canvas account (all courses) and should not be shared or exposed publicly. Set an expiration date for the token, so that it's no longer valid at all after a certain date. If you believe your token has been compromised, you can delete it in your Canvas settings.
:::

#### Downloading the Scripts

There are two related Python scripts that are needed for this conversion. Download them from the links below. You will likely need to right-click (Windows) or control-click (Mac) on the links and choose "Save link as..." to save them to your computer. Then move them into your `PL-UMICH-<course_name>` folder.

- <a href="https://raw.githubusercontent.com/PrairieLearn/PrairieLearn/master/contrib/question_converters/canvas/quiz2pl.py" download="quiz2pl.py">quiz2pl.py</a>
- <a href="https://raw.githubusercontent.com/PrairieLearn/PrairieLearn/master/contrib/question_converters/canvas/canvas.py" download="canvas.py">canvas.py</a>

### Preparing Your Development Environment

There's a bit of one-time setup we need to do so that you can run the tool. The instructions below assume you're using VS Code. If you're using a different IDE, the steps will be similar, but you may need to adapt them.

- Open VS Code.
- Choose File > Open Folder... and choose your PrairieLearn repo folder. The name of the folder should be `PL-UMICH-<course_name>`, where `<course_name>` is the short name of your course.
- Choose Terminal > New Terminal. A window at the bottom will open. 
- When you installed Python, you got a program that's called either `python` or `python3`. We need to figure out which one you have. In the terminal, type `python --version` (that's two dashes) and hit <kbd>Enter</kbd>. If you see a version number, then you have `python`. If you see an error, try `python3 --version`. If that works, then you have `python3`. If neither works, then either Python isn't installed or something is broken.
- In the instructions that follow, I'll simply write `python`, but if you have `python3`, then use that instead.
- In the terminal area, we need to create a _Python virtual environment_ where we can install tools that the Canvas conversion tool requires. Enter the following command into the terminal and hit <kbd>Enter</kbd>:
    ```bash
    python -m venv myenv
    ```
- This should create a new folder named `myenv` in your repo folder. If everything worked correctly, there is otherwise no output from this command. If you instead see any text, you might try deleting the `myenv` folder, closing VS Code, reopening it, and trying the command again. If you still have trouble, please reach out to me for help.
- Next, we need to "activate" the virtual environment. The way to do that depends on your operating system. For Windows, type the following and hit <kbd>Enter</kbd>:
    ```bash
    myenv\Scripts\activate
    ```
    For Mac, enter:
    ```bash
    source myenv/bin/activate
    ```
- If this worked, you should see `(myenv)` at the beginning of the line in the terminal.
- Now we can install the Python tools that the Canvas conversion tool needs. The program that allows us to do this is called `pip` (if you have `python`) or `pip3` (if you have `python3`). Enter the following command (or the `pip3` version if needed) into the terminal and hit <kbd>Enter</kbd>:
    ```bash
    pip install requests
    ```
- You should see messages something like the following:
    ```bash
    Collecting requests
    ... [lots of text omitted]
    Successfully installed ... [more text omitted]
    ```

### Getting Your PL Course Instance Name

A PrairieLearn _course_ can consist of multiple PrairieLearn _instances_ -- generally there is one instance per semester. To find your instance name, look in the list of files in the "Explorer" tab on the left sidebar of VS Code. Find the folder called `courseInstances`. You should have one folder per course instance inside that folder. For example, you might have a folder inside `courseInstances` called `F26` for the Fall 2026 semester. Make a note of the name of the folder for the course instance you want to import your Canvas quiz into. We'll need that in the next step.

### Publish Your Canvas Course

The conversion tool only works for published Canvas courses. If your course is not published, please publish it before proceeding, even if this is just a temporary step to allow the conversion tool to work. You can unpublish it later if you wish.

### Running the Canvas Import Tool

If you still have your terminal window open from the previous section, you can continue there. Otherwise, choose Terminal > New Terminal in VS Code. After a delay of couple seconds, the terminal prompt should say `(myenv)` at the beginning of the line, indicating that your virtual environment is active. If it doesn't, then you activate it with the command `myenv\Scripts\activate` (Windows) or `source myenv/bin/activate` (Mac).

We're ready to run the tool! In the terminal window, with the `myenv` virtual environment active, we'll need to enter the command `python quiz2pl.py . courseInstance`. Note:

- Replace `python` with `python3` if needed.
- There is a space before and after the period in the middle of the command.
- Replace `courseInstance` with the name of the course instance you found in the previous step, e.g., `F26`.

Enter the command into the terminal and hit <kbd>Enter</kbd>. You should see the message:

```bash
Reading data from Canvas...
 0: ...
 ...
 Which course? 
```

with a list of _published_ courses you have in Canvas, numbered sequentially starting with 0. Enter the number corresponding to the course you want to import from and hit <kbd>Enter</kbd>.









### More Details in the Official Documentation

The above steps will likely be sufficient for most use cases, but note the [official Canvas import tool documentation](https://github.com/PrairieLearn/PrairieLearn/tree/master/contrib/question_converters/canvas) in case you would like to see more advanced options.