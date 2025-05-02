**Project Overview:**

Lola's 2.0 is a full stack web application that is currently not
deployed, meaning it must be on a local computer to run. It consists of
a frontend and a backend, both which must be running for the application
to then run. If the client so chooses, they can deploy the application
using AWS, as initially outlined. As for future incurred costs, the AWS
API does use a token system to charge for calls, which the client
already is aware of and is paying for. If the client wants to deploy,
there will also be incurred costs for hosting and for the domain,
depending on where they deploy. Navigate to the project repository's
README.md to see more information about the project and setup. Local
Setup is also included below.

**Local Setup Instructions:**

1.  In order to run the project, you must first get the proper access
    credentials from Amazon Web Services (AWS) to make calls to the AI
    API

2.  On AWS Console, select right region:

    a.  On the top panel of the screen after logging in, make sure the
        region is 'United States (N. Virginia' (us-east-1)

3.  Request access to model

    a.  Search 'Bedrock' on AWS Console

    b.  Scroll all the way down and click 'Model access' on left panel
        of screen

    c.  For our use case, we requested access to the 'Nova Pro' model
        which is what's used in the project

4.  Create IAM User so you can call bedrock on your local settings:
    [follow this tutorial to the 3 minute
    mark](https://www.youtube.com/watch?v=524J-y04Kx0)

5.  Download [AWS
    CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)

6.  After it downloads, open any terminal and type 'aws configure'

    a.  You will be prompted to enter

        i.  AWS Access Key ID

        ii. AWS Secret Access Key

        iii. Default Region Name: us-east-1

        iv. Output format: just hit enter to skip

    b.  To get the access key ID and secret access key:

        i.  Go back to IAM on AWS console

        ii. Click on 'users' on left panel of screen

        iii. Click the user you created from before with the youtube
             guide

        iv. Scroll down and click "create access key"

        v.  For use case, choose 'local code', confirm and hit next, and
            give it a name

        vi. It will now display the keys. Copy and paste them to their
            respective fields in your terminal.

        vii. IMPORTANT: the keys will be configured to your local system
             (usually in a folder called 'aws') but once you close this
             tab, you won't be able to see the secret access key again
             unless you manually find it in your system

        viii. The youtube video linked above walks through this entire
              written process as well (aside from downloading AWS CLI)

7.  Download the [VSCode](https://code.visualstudio.com/)
    code editor

8.  Download [python](https://www.python.org/downloads/)
    (ensure to check the add to python to PATH during installation)

9.  Download [Node.js](https://nodejs.org/en/download)
    (can either install through terminal or install pre-built version)

10. Download [git](https://git-scm.com/)

11. Restart computer

12. In VSCode, open Extensions and install Python, Pylance and Python
    Debugger


13. Navigate to the Lola's 2.0 GitHub repository:
    [https://github.com/lolas-2/Lolas-2.0](https://github.com/lolas-2/Lolas-2.0)

14. Click the green Code button on the top right and copy the HTTPS url
    to your clipboard

15. In VSCode, select the clone repository button, and paste in the url
    link you previously copied; this should clone the repository

    a.  You can either clone directly in VSCode or in separate terminal
        with the command git clone \<insert copied url\>

16. Once it's open in VSCode, create a Python virtual environment with
    dependencies installed:

    a.  On Windows

        i.  Type into terminal: **python -m venv .venv**

        ii. To activate, type into terminal: **cd .venv** *then*
            **Scripts/Activate.ps1**

        iii. In terminal: **pip install -r requirements.txt** to install
             dependencies

        iv. If for some reason installing all in requirements.txt
            doesn't work, you can install each thing separately in the
            terminal. This applies for Mac setup as well

            1.  pip install fastapi, pip install pandas, pip install os,
                pip install fuzzywuzzy, pip install python-Levenshtein,
                pip install pytest, pip install httpx, pip install
                scikit-learn, pip install numpy, pip install rapidfuzz,
                pip install langgraph, pip install langchain, pip
                install langchain-community, pip install langchain-aws,
                pip install boto3, pip install langchain-core, pip
                install pydantic

    b.  On Mac:

        i.  Type into terminal: **python -m venv .venv**

        ii. To activate: **source .venv/bin/activate**

        iii. In terminal: **pip install -r requirements.txt** to install
             dependencies

    c.  Or using the command palette:

        i.  Press Ctrl+Shift+P (Windows/Linux) or Cmd+Shift+P (Mac)

        ii. Choose python interpreter (the one associated with your
            venv)

        iii. It will offer to install dependencies located in
             requirements.txt file (choose it)

**Important:**

- In your terminal, you should see the 'venv' prefix. Example shown
  below:

  - **(.venv)** PS C:\\Path\\To\\Repo\\Lolas-2.0\>

- At the bottom right of screen, make sure the python interpreter chosen
  is the venv one

- Refresh your window: view -\> command palette -\> Developer: Reload
  Window

\*\*Note: the 'cd' commands are on the assumption that you are in the
root folder. So your terminal says something like this:
C:\\path\\to\\Lolas-2.0\>

17. Open a new terminal, navigate into the backend folder (**cd
    src/backend**) and paste in the following command to start the
    application's backend: **uvicorn main:app --reload**

18. Open a new terminal, navigate into the frontend folder
    (**cd/src/frontend**) and paste in the following command to install
    frontend dependencies: **npm install**

    a.  Then start the application's frontend: **npm run dev**

19. Your project should now be running on a localhost (link provided
    when you started the frontend), which you can view from any browser

**Data Cleaning**

We cleaned our original data file - a stock of products - according to
our client's specifications by standardising the nutrient columns
(sodium, sugar, saturated fats, trans fat, carbohydrates, salt, fibre
and proteins) per 100 using the product's serving size and creating
flags based on this to determine if the product is high or low in these
nutritional qualities.

**Backend Structure**

We have three API endpoints feeding data to the frontend found in main.py in src/backend

- /grocery

  - Handles the initial AI ranking when a user searches for a product
    using layman terms (ie. pepperoni pizza)

  - The service layer for the logic is handled in chat_service.py

  - Request body:

> { \"search_string\": \"string\"} -\> replace "string" with a layman
> product search (like 'pepperoni pizza')

- /recommendations

  - Handles manual recommendations of a product by nutrition attribute
    column. The user clicks on a product, and they can choose which
    nutrition attribute to base recommendations on (low sugar, low
    calories, low saturated fat, low sodium, nns, and ultra processed)

  - The service layer for the logic is handled in
    recommendation_service.py. Specifically: get_closest_product_name
    and recommendations_by_column

  - Request body:

> { \"product_name\": \"string\",
>
> \"column_name\": \"string\"}

- Replace the 'string' of product_name with specific product name (get
  from 'product' column in cleaned_data_4 excel)

- Replace 'string' of column name with EXACTLY sugar, calories,
  saturated fat, sodium, ultraprocessed, nns)

<!-- -->

- /ai-recommendations

  - Handles AI recommendations. The AI prompt combines all the nutrition
    attributes columns so recommendations are not based on a single
    nutrition attribute column, unlike the one above

  - The service layer for the logic is handled in
    recommendation_service.py. Specifically: prompt, tools, and
    getRecommendationResponse

  - Request body:

> { \"full_product_name\": \"string\"} -\> replace 'string' with
> specific product name (get from 'product' column in cleaned_data_4
> excel)

- To interact with only these APIs and not the application as a whole
  (frontend excluded), after you start up the backend (step 16), you can
  click the link it provides in the terminal. When it opens in browser,
  add '/docs' to the end of the url

**Running Backend Tests**

The tests are found in src/backend/tests.

Two ways to run:

1)  (preferred): Use the **Testing** panel (beaker icon) on the left
    side panel of VSCode. Here all the tests should load and you can run
    all the tests individually or together

2)  Run the following command in the terminal from the root folder:
    **python -m pytest**

    a)  The root folder follows a path similar to
        C:\\path\\to\\Lolas-2.0\>

**Frontend Structure**

The interface is split into main pages:
1. Home Page (Home.jsx)

This page has the entry point for the grocery interface and contains a
search bar where users can make their product queries. This page then
navigates to a page with the all the product cards from the user's query
organised according to the healthiest nutritional rankings. The
information on this page is pulled from **/grocery** API route in the
backend.

2. Product Details Page (ProductDetail.jsx)

This page appears after clicking a certain product card in the home
page. It displays the details of the products: name, price, image and
nutritional details. At the end of this page, the recommendations for
similar products are displayed in product cards as well. These
recommendations are split into manual recommendations (filtered from
nutritional flags in original data file) and AI recommendations. This
information is pulled from the /recommendations and /ai-recommendations
API routes respectively.

**Running Frontend Tests**

The tests are found in src/frontend/src/tests

- Navigate to **cd/src/frontend**

- To run, type into terminal:

  - **npm install -D vitest jsdom \@vitest/ui \@testing-library/dom
    \@testing-library/jest-dom**

  - **npx vitest**
