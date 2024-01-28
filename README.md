# Facebook Groups Post Bot

# Install

## Prerequisites

* [Google chrome](https://www.google.com/intl/es-419/chrome/)
* [Python >=3.10](https://www.python.org/)
* [Git](https://git-scm.com/)

## Installation

1. Clone the repo

   ```sh
   https://github.com/criticalRobin/facebook_auto_poster.git
   ```

2. Install python packages (opening a terminal in the project folder)

   ```sh
   python -m pip install -r requirements.txt 
   ```

3. Create a `.env` file and `data.json` file in the project folder.

# Settings

Update your chrome path in the `.env` file (note: the chrome path is the folder where chrome data its installed)

```js
CHROME_PATH = C:Users<<your-user-name>>AppDataLocalGoogleChromeUser Data
```

# Run
1. Open the "data.json" file, and add the groups where you want to post, and the text of the post in the "text" field

    ```json
        {
        "posts": [
            {
                "text": "text post 1",
                "image": "{image path}"
            },
            {
                "text": "text post 2",
                "image": "{image path}"
            },
            {
                "text": "text post 3",
                "image": ""
            },
        ],
        "groups": [
            "https://www.facebook.com/groups/sample-group-1/",
            "https://www.facebook.com/groups/sample-group-2/",
            "https://www.facebook.com/groups/sample-group-3/",
            "https://www.facebook.com/groups/sample-group-4/",
            "https://www.facebook.com/groups/sample-group-5/",
            "https://www.facebook.com/groups/sample-group-6/",
            "https://www.facebook.com/groups/sample-group-7/",
            "https://www.facebook.com/groups/sample-group-8/"
        ]
    }
    ```

2. Run the **post_groups**.py script

    ```sh
    python __post_groups__.py
    ```

3. Wait until the script finish, and enjoy your posts in the groups 
