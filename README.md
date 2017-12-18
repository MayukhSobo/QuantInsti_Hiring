<h1 id="quantinsti-hiring">QuantInsti Hiring</h1>
<p>Implementation of the complete stack for getting the data and then implementing a trading strategy.</p>
<h1 id="implementation">Implementation</h1>
<p>There are two origin files to start the program. The complete project is divided into two section to emulate real Algorithmic Trading Engines. It has one <strong><a href="http://server.py">server.py</a></strong> to that acts as an exchange server between a program engine and the trader. It handles all the request and without the assistance of server, one can not make transactions.</p>
<p>The other main section is <strong><a href="http://main.py">main.py</a></strong>  which actually starts the program.</p>
<h2 id="python-and-virtualenv">Python and Virtualenv</h2>
<ul>
<li><em>Python3.6</em> or above</li>
<li><em>virtualenv 15.1</em> or above</li>
</ul>
<h2 id="environment">Environment</h2>
<ul>
<li>Install the <em>virtualenv</em> using <em>pip</em> using the following command</li>
</ul>
<pre class=" language-sh"><code class="prism  language-sh">$ pip3 install virtualenv
</code></pre>
<ul>
<li>Then create a virtualenv with any name say <strong>env</strong></li>
</ul>
<pre class=" language-sh"><code class="prism  language-sh">$ virtualenv -p python3.6 --no-site-packages env
</code></pre>
<ul>
<li>Activate the Virtual Environment</li>
</ul>
<pre class=" language-sh"><code class="prism  language-sh">$ source ./env/bin/activate
</code></pre>
<ul>
<li>Finally install the dependencies from the <em>requirement.txt</em> file</li>
</ul>
<pre class=" language-sh"><code class="prism  language-sh">$ pip install -r requirement.txt 
</code></pre>
<h2 id="data">Data</h2>
<p>If input dataset is not mentioned then, it pulls the data from <a href="www.quandl.com"><strong>Quandl</strong></a>. We can also pass the input data while running our program. The Quandl parameters like <em>api-key</em> or <em>company</em> should be given form <strong><a href="http://constants.py">constants.py</a></strong> file.</p>
<p>The portfolio data is also saved into a csv file named <strong>portfolio.csv</strong> inside the data folder.</p>
<p><strong>To provide your own dataset, please put the csv file into the data folder and mention the name of the csv file without the path. Do not name your csv file as <code>stock_data.csv</code></strong></p>
<h2 id="running-the-program">Running the Program</h2>
<ul>
<li><strong>Run the exchange server</strong>
<ul>
<li>Open a terminal</li>
<li>Navigate to the directory</li>
<li>Activate the virtualenv using <code>source ./env/bin/activate</code></li>
<li>Run the server using <code>python server.py [port]</code></li>
</ul>
</li>
<li><strong>Run the Engine</strong>
<ul>
<li>Open Another terminal</li>
<li>Navigate to the directory</li>
<li>Activate the virtualenv using <code>source ./env/bin/activate</code></li>
<li>Run the engine using <code>python main.py initial_capital [input_data]</code></li>
</ul>
</li>
</ul>
<h2 id="exit">Exit</h2>
<p>The Sever program never exits because it continues to server for any incoming order update. To exit it, we need to kill it manually.</p>
<p>The main engine however kills itself it <em>line-end</em> comes in the dataset or we kill it manually.</p>
<h1 id="reflection">Reflection</h1>
<ul>
<li>The Trading Strategy function is minimal as it should be but still bit coupled with the existing code. We should decouple it so that it can operate as a plug and play method.</li>
<li>With SMA-LMA model, we are either selling all the stocks or spending all the money to buy stocks. However this can and should be limited.</li>
<li>The exchange server is not multi-threaded and hence it can not handle multiple requests. This can be improved with python’s new <strong>asyncio</strong> features.</li>
<li>Some paths and parts are still hard coded which can be improved.</li>
<li>Instead of running two separate files(server and main engine), we can integrate both of them together.</li>
</ul>

