## Weather info service
### Project based on [accuweather API](https://developer.accuweather.com/)
[API Reference](https://developer.accuweather.com/apis)

### To use
#### Step 1: Clone the Repository

Clone the project repository to your local machine:

```bash
git clone https://github.com/SerezhaK/cu_project_homework
cd repository
```
#### Step 2: Create a Virtual Environment
Create a virtual environment:

```bash
python -m venv venv
```
Activate the virtual environment:
On Windows:
```bash
venv\Scripts\activate
```
On macOS/Linux:
```bash
source venv/bin/activate
```
#### Step 3: Install Dependencies and add API key
Install the required packages using pip:
```bash
pip install -r requirements.txt
```
```bash
echo ACCUWEATHER_API_KEY=$YOUR_API_KEY > .env
```
#### Step 4: Run the Project
```bash
python main.py
```