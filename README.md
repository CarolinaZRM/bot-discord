<h1> Bot Orientador UPRM </h1>
<h2> Fully Autonomous Discord Bot for a Server </h2>
<h3> Creators: Team MADE </h3> 

<h2> Configuration </h3>
<p>
  The project needs a `.env` file with the appropriate values. If a required value is not present the application will not start.

  The application environment variables to be assigned into a `.env` file are in [.env.examples](.env.example)
</p>

<details>
  <summary>Activating Virtual Environments</summary>

  <ul>
	<li>For users to properly install dependencies for this application, a Virtual Environment is needed so all packages can be used properly</li>
  <li>
    For Windows 10 users:
    <ol>
      <li>Enter in the Command Prompt: <code>python -m venv venv/</code></li>
      <li>To activate Virtual Environed, type in the Command Prompt:  <code>venv\Scripts\activate</code></li>
      <li>To install project dependencies, type in the Command Prompt: <code> pip install -r requirements.txt</code></li>
      <li>To deactivate Virtual Environment, type in the Command Prompt: <code>deactivate</code></li>
    </ol>
  </li>
  
  <li>
    For macOS & Linux users:
    <ol>
      <li>Enter in the Terminal: <code>python -m venv venv/</code></li>
      <li>To activate Virtual Environment, type in the Terminal:  <code>source venv/bin/activate</code></li>
      <li>To install project dependencies, type in the Terminal: <code> pip install -r requirements.txt</code></li>
      <li>To deactivate Virtual Environment, type in the Terminal : <code>deactivate</code></li>
    </ol>
  </li>
 </ul>
  
</details>


## Testing

Run: `python -m unittest discover -s tests -t .` from the top level directory

For mocking the MongoDB Database for testing create a `.env.development` file and change the connection string to any of your choosing. The one I use is  

```env
MONGO_CONNECTION_STRING=mongodb://test.db
```