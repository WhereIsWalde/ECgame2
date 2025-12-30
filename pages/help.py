import streamlit as st

st.set_page_config(layout="centered")
st.header("Documentation of the National Economy Game")

with st.container(border=True):
    st.markdown(
    """
    <h2 style="font-family:serif;">Starting situation</h2>
    <div style="font-family: 'Courier New', Courier, monospace; color: #FFFFFF;">
        <p>Your country is in a very bad position. Previous governments have not put an
        effort into improving and developing the country. It is up to you to solve the
        problems that your country is facing and finally improve the living standard
        of the poor citizens to match that of the developed western democracies.</p>
        The previous governments have practiced very poor policies. By continuing
        with the same policies and not changing anything, your country's forecast is
        grim:
        <ul style="font-family: 'Courier New', Courier, monospace; font-size:17px;">
            <li>The population will keep growing. A larger population needs more of
                everything, but your country's natural resources are limited.</li>
            <li>The environment will keep deteriorating. It is already having a negative
                effect on farming productivity and the death rate of citizens.</li>
            <li>Government debt will increase at an exponential pace, as your country
                pays interest on interest. The amount of debt is already double what the
                country can safely afford and the interest rate of the debt has increased
                to 15%.</li>
            <li>Agricultural production will slowly deteriorate due to the poor state of
                the environment.</li>
            <li>Energy production will stay stagnant.</li>
            <li>Goods production will stay stagnant.</li>
            <li>Foreign humanitarian organizations will have to intervene to distribute
                food to starving citizens.</li>
        </ul>
    </div>
    """, 
    unsafe_allow_html=True
)
    
# --- DECISIONS SECTION ---
with st.container(border=True):
    st.markdown(
    """
    <h2 style="font-family:serif;">Decisions</h2>
    <div style="font-family: 'Courier New', Courier, monospace; color: #FFFFFF;">
        <p>The game is played in a series of 5 year cycles. You will receive information
        of the current situation at the beginning of each cycle. This information
        includes the resources that you have available for distribution during the
        cycle and the capacity levels built so far. Resources include food, goods, and
        energy.</p>
        <p>After studying the current situation it's time to make decisions that will lead
        your people to a better future. These decisions are:</p>
        <ul style="font-family: 'Courier New', Courier, monospace; font-size:17px;">
            <li>1. Distributing food for the people</li>
            <li>2. Distributing goods and specials for the people</li>
            <li>3. Investing goods in infrastructure</li>
            <li>4. Allocating energy to agriculture and industry</li>
            <li>5. Dividing farming area and production capacity</li>
            <li>6. Exporting and importing food, goods and energy</li>
            <li>7. Financial affairs</li>
        </ul>
        <p>After the decisions are made and the five year cycle is completed, you will
        receive output describing your country's current situation. Some of the output 
        tells you how well you succeeded during the last five years and some of it 
        tells you your country's current situation.</p>
    </div>
    """, 
    unsafe_allow_html=True
)

# --- DISTRIBUTING FOOD ---
with st.container(border=True):
    st.markdown(
    """
    <h2 style="font-family:serif;">1. Distributing Food for the People</h2>
    <div style="font-family: 'Courier New', Courier, monospace; color: #FFFFFF;">
        <p><strong>Low quality food</strong> (potatoes, rice and vegetables) and <strong>high quality food</strong> 
        (beef, pork, chicken and preprocessed food) represent the resources you can use to
        feed your people. If there is anything left of these resources after you have
        decided how much to distribute, it is automatically exported.</p>
        <p>You can't store the food for later use. Note that one cycle in the game corresponds to a
        period of five years. The food that you distribute is spread out evenly during
        the five years. You are required to give the total amount for the five year
        cycle in the input.</p>
        <p>The amount of food available in the next cycle depends on the amount of LQ
        food and HQ food produced and imported. Remember to take care that you
        really have something to distribute in the following cycle.</p>
    </div>
    """, 
    unsafe_allow_html=True
)

# --- DISTRIBUTING GOODS ---
with st.container(border=True):
    st.markdown(
    """
    <h2 style="font-family:serif;">2. Distributing Goods and Specials</h2>
    <div style="font-family: 'Courier New', Courier, monospace; color: #FFFFFF;">
        <p><strong>Specials</strong> (tobacco, coffee and cocoa) are agricultural products, but they are
        regarded as material welfare rather than food when distributed to the
        people. The specials that are not distributed to the people are automatically
        exported.</p>
        <p><strong>Low quality goods</strong> are building material, handcraft and simple electric
        appliances. <strong>High quality goods</strong> are domestic appliances, electronics, 
        artificial materials and immaterial products.</p>
        <p>Goods are produced in the country's factories and offices (goods production capital).
        LQ goods, HQ goods, and specials are treated similarly when distributed to citizens, 
        but the utility per item differs and changes as the country develops.</p>
    </div>
    """, 
    unsafe_allow_html=True
)

# --- INVESTING GOODS ---
with st.container(border=True):
    st.markdown(
    """
    <h2 style="font-family:serif;">3. Investing Goods in Infrastructure</h2>
    <div style="font-family: 'Courier New', Courier, monospace; color: #FFFFFF;">
        <p>You can invest both HQ goods and LQ goods in the following sectors:</p>
        <ul style="font-family: 'Courier New', Courier, monospace; font-size:17px;">
            <li>Fossil Fuel Production under Construction</li>
            <li>Nuclear Power Production under Construction</li>
            <li>Renewable Energy Production under Construction</li>
            <li>New Investments to Energy Efficiency</li>
            <li>New Investments to Environmental Protection</li>
            <li>Food Production under Construction</li>
            <li>Goods Production under Construction</li>
            <li>New Investments to Human Services</li>
        </ul>
        <p>There is no difference between low quality and high quality goods in terms of
        investment; each will have exactly the same effect per item. High quality
        goods are prioritized in investments. Any LQ goods available after
        distributing and investing are automatically exported.</p>
    </div>
    """, 
    unsafe_allow_html=True
)

# --- ALLOCATING ENERGY ---
with st.container(border=True):
    st.markdown(
    """
    <h2 style="font-family:serif;">4. Allocating Energy</h2>
    <div style="font-family: 'Courier New', Courier, monospace; color: #FFFFFF;">
        <p>You must provide energy to produce food, specials and goods. You can't expect
        to get maximum output from the production sectors if you are not providing
        enough energy. The actual production capacity is directly dependent on the 
        ratio of energy allocated and energy needed.</p>
        <p>You can also carry some of your fossil fuel reserves over to the next cycle.
        Electricity cannot be carried over. Because you can spend two kinds of energy 
        it is required that you specify the amount of electricity exported.</p>
    </div>
    """, 
    unsafe_allow_html=True
)

# --- DIVIDING AREA ---
with st.container(border=True):
    st.markdown(
    """
    <h2 style="font-family:serif;">5. Dividing Farming Area and Production</h2>
    <div style="font-family: 'Courier New', Courier, monospace; color: #FFFFFF;">
        <p>Your country has a fixed amount of farming area. Specify a number between 0 and 1 for
        both 'Farming Area Producing Hq Food' and 'Farming Area Producing Specials'.
        Note that the sum of the two may not exceed one. The rest is allocated for LQ food.</p>
        <p>You can also redirect your manufacturing plants. Specify a number between 0 and 1 for 
        'Fraction of Industry Producing HQ Goods'. If the number is below one, the rest 
        of the capacity is used to produce LQ goods.</p>
    </div>
    """, 
    unsafe_allow_html=True
)

# --- EXPORTING AND IMPORTING ---
with st.container(border=True):
    st.markdown(
    """
    <h2 style="font-family:serif;">6. Exporting and Importing (Trade)</h2>
    <div style="font-family: 'Courier New', Courier, monospace; color: #FFFFFF;">
        <p>Trading is the key to successful development. The effect of trade on development 
        depends on your share of the world market and the power of your country. 
        Trading is like a zero sum game: if you manage to increase your share above the average, 
        someone else's share will be below the average.</p>
        <p>Because trade consists of both imports and exports, it is possible to import
        and export the same product to occupy a bigger share. However, the exporting
        price is only 95% of the importing price.</p>
        <p>The prices of the items traded are based on demands and offerings. Exporting a 
        lot of one product will eventually push down the price. Importing loads without 
        anyone exporting equally much will cause the price to go up.</p>
    </div>
    """, 
    unsafe_allow_html=True
)

# --- FINANCIAL AFFAIRS ---
with st.container(border=True):
    st.markdown(
    """
    <h2 style="font-family:serif;">7. Financial Affairs</h2>
    <div style="font-family: 'Courier New', Courier, monospace; color: #FFFFFF;">
        <p>'Amortization of Debts' is the amount by which you are willing to amortize
        your debts. Debts can be amortized by trade surplus or by sacrificing
        your investments abroad.</p>
        <p>If the trade surplus is negative, the market will take its money. If you are 
        unable to pay for the trading deficit, you will be granted an extra loan that is 
        added to your existing debts.</p>
    </div>
    """, 
    unsafe_allow_html=True
)

# --- SOCIAL SECTOR ---
with st.container(border=True):
    st.markdown(
    """
    <h2 style="font-family:serif;">Social Sector: Human Services</h2>
    <div style="font-family: 'Courier New', Courier, monospace; color: #FFFFFF;">
        <p>Investing goods into the social sector (Health Care, Education) increases general welfare.
        Increasing this will drop the birth rate closer to the natural birth rate of 10 births 
        per 1000 population.</p>
        <p>Educated citizens are more productive. Up to half of the investments can be
        lost if the country trades nothing during the cycle. Depreciation of human services 
        capital is only 10% per cycle.</p>
    </div>
    """, 
    unsafe_allow_html=True
)

# --- MATERIAL WELFARE ---
with st.container(border=True):
    st.markdown(
    """
    <h2 style="font-family:serif;">Material Welfare & Utility</h2>
    <div style="font-family: 'Courier New', Courier, monospace; color: #FFFFFF;">
        <p>Increasing the level of goods spent on material welfare increases the use of
        energy among the population. When living standard begins to rise, people will start
        demanding better quality goods and specials.</p>
        <p><strong>Utility Table (Distribution per capita):</strong></p>
        <table style="width:100%; border: 1px solid white; color: white;">
          <tr>
            <th style="border: 1px solid white; text-align: left;">Type</th>
            <th style="border: 1px solid white;">0</th>
            <th style="border: 1px solid white;">10</th>
            <th style="border: 1px solid white;">20</th>
            <th style="border: 1px solid white;">200</th>
          </tr>
          <tr>
            <td style="border: 1px solid white;">Low Quality</td>
            <td style="border: 1px solid white;">3.00</td>
            <td style="border: 1px solid white;">1.50</td>
            <td style="border: 1px solid white;">0.00</td>
            <td style="border: 1px solid white;">0.00</td>
          </tr>
          <tr>
            <td style="border: 1px solid white;">High Quality</td>
            <td style="border: 1px solid white;">0.00</td>
            <td style="border: 1px solid white;">1.80</td>
            <td style="border: 1px solid white;">3.60</td>
            <td style="border: 1px solid white;">0.00</td>
          </tr>
          <tr>
            <td style="border: 1px solid white;">Specials</td>
            <td style="border: 1px solid white;">1.50</td>
            <td style="border: 1px solid white;">1.50</td>
            <td style="border: 1px solid white;">1.50</td>
            <td style="border: 1px solid white;">0.00</td>
          </tr>
        </table>
        <br>
        <p>The total utility is a sum of utility gained from LQ goods, HQ goods, and specials.</p>
    </div>
    """, 
    unsafe_allow_html=True
)

# --- NUTRITION ---
with st.container(border=True):
    st.markdown(
    """
    <h2 style="font-family:serif;">Nutrition</h2>
    <div style="font-family: 'Courier New', Courier, monospace; color: #FFFFFF;">
        <p>If people don't get enough food, they'll begin to starve. When people get more 
        than 7.5 units of food per capita, starvation stops. If distribution is below 
        2 units, foreign humanitarian organizations will intervene.</p>
        <p><strong>Food Utility Table (Distribution per capita):</strong></p>
        <table style="width:100%; border: 1px solid white; color: white;">
          <tr>
            <th style="border: 1px solid white; text-align: left;">Type</th>
            <th style="border: 1px solid white;">0</th>
            <th style="border: 1px solid white;">10</th>
            <th style="border: 1px solid white;">20</th>
            <th style="border: 1px solid white;">90</th>
          </tr>
          <tr>
            <td style="border: 1px solid white;">Low Quality</td>
            <td style="border: 1px solid white;">4.00</td>
            <td style="border: 1px solid white;">2.00</td>
            <td style="border: 1px solid white;">0.00</td>
            <td style="border: 1px solid white;">0.00</td>
          </tr>
          <tr>
            <td style="border: 1px solid white;">High Quality</td>
            <td style="border: 1px solid white;">0.00</td>
            <td style="border: 1px solid white;">2.00</td>
            <td style="border: 1px solid white;">1.75</td>
            <td style="border: 1px solid white;">0.00</td>
          </tr>
        </table>
    </div>
    """, 
    unsafe_allow_html=True
)

# --- ENVIRONMENT ---
with st.container(border=True):
    st.markdown(
    """
    <h2 style="font-family:serif;">Energy Efficiency & Environment</h2>
    <div style="font-family: 'Courier New', Courier, monospace; color: #FFFFFF;">
        <p>Energy efficiency is directly related to the environment. More efficient
        machines produce less pollution. The efficiency multiplier can go from 0.3 
        (excellent) to 1.3 (neglected).</p>
        <p>The quality of the environment is represented as a value between 0.0 (destroyed)
        and 1.0 (excellent). If the environment drops below 0.7, it causes death rates 
        to rise. The environment can heal itself, with the peak healing rate occurring 
        at quality 0.5.</p>
    </div>
    """, 
    unsafe_allow_html=True
)

# --- ENERGY PRODUCTION ---
with st.container(border=True):
    st.markdown(
    """
    <h2 style="font-family:serif;">Energy Production</h2>
    <div style="font-family: 'Courier New', Courier, monospace; color: #FFFFFF;">
        <p><strong>Fossil Fuels:</strong> Low investment, moderate depreciation (20%), 
        causes pollution.</p>
        <p><strong>Nuclear Power:</strong> Moderate investment, high depreciation (25%), 
        low pollution. Requires high education to be safe. Unsafe plants increase risk.</p>
        <p><strong>Renewable Energy:</strong> Large investments, low depreciation (15%), 
        low pollution. Variable production capacity.</p>
    </div>
    """, 
    unsafe_allow_html=True
)

# --- FOOD PRODUCTION ---
with st.container(border=True):
    st.markdown(
    """
    <h2 style="font-family:serif;">Food Production</h2>
    <div style="font-family: 'Courier New', Courier, monospace; color: #FFFFFF;">
        <p><strong>LQ Food:</strong> High yield (avg 28 units), weather dependent.</p>
        <p><strong>HQ Food:</strong> Lower yield (1/3 of LQ), less weather dependent.</p>
        <p><strong>Specials:</strong> Moderate yield (1/2 of LQ), cannot feed people, weather dependent.</p>
        <p>Food production capital depreciation is 20% per cycle.</p>
    </div>
    """, 
    unsafe_allow_html=True
)

# --- GOODS PRODUCTION ---
with st.container(border=True):
    st.markdown(
    """
    <h2 style="font-family:serif;">Goods Production</h2>
    <div style="font-family: 'Courier New', Courier, monospace; color: #FFFFFF;">
        <p>Industrial production produces twice the pollution as farming. 
        <strong>HQ Goods</strong> production depends heavily on high-tech equipment (robotics)
        and education level.</p>
        <p>Successful know-how exchange (Trade) can increase the benefits from robotics considerably.</p>
    </div>
    """, 
    unsafe_allow_html=True
)

# --- DEBT AND INVESTMENTS ---
with st.container(border=True):
    st.markdown(
    """
    <h2 style="font-family:serif;">Debt and Foreign Investment</h2>
    <div style="font-family: 'Courier New', Courier, monospace; color: #FFFFFF;">
        <p>The interest rate of the debt is directly proportional to the amount of
        debt your country can afford. Max interest is 25%. There is no limit to the 
        amount of debt, but high debt increases Risk.</p>
        <p>Profit from investments abroad goes from 5% up to 40% per cycle, depending 
        on the education level of your economists.</p>
    </div>
    """, 
    unsafe_allow_html=True
)

# --- SCORING ---
with st.container(border=True):
    st.markdown(
    """
    <h2 style="font-family:serif;">Scoring</h2>
    <div style="font-family: 'Courier New', Courier, monospace; color: #FFFFFF;">
        <p>The score reflects living standard, future expectations, and environment quality.</p>
        <p><strong>Formula:</strong> Score = Env * (1/UTF + 4/UTGS + Risk + 5*Deaths)^0.3</p>
        <p>Theoretic maximum score is ~2.426. A score below 0.5 is considered a failure.</p>
    </div>
    """, 
    unsafe_allow_html=True
)

