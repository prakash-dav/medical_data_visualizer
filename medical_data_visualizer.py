# Step 1: आवश्यक लाइब्रेरीज़ आयात करें
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Step 1: डेटा लोड करें
df = pd.read_csv('medical_examination.csv')  # CSV फ़ाइल को DataFrame में लोड करें

# Step 2: overweight कॉलम बनाएं
df['bmi'] = df['weight'] / ((df['height'] / 100) ** 2)  # BMI की गणना करें
df['overweight'] = (df['bmi'] > 25).astype(int)  # 25 से अधिक BMI वाले मरीजों के लिए overweight को 1 सेट करें

# Step 3: कोलेस्ट्रॉल और ग्लूकोज डेटा को सामान्य करें
df['cholesterol'] = df['cholesterol'].apply(lambda x: 0 if x == 1 else 1)  # 1: सामान्य को 0 में सेट करें, अन्यथा 1
df['gluc'] = df['gluc'].apply(lambda x: 0 if x == 1 else 1)  # 1: सामान्य को 0 में सेट करें, अन्यथा 1

# Step 4: कैटिगोरिकल प्लॉट बनाने के लिए फ़ंक्शन बनाएं
def draw_cat_plot():
    # Step 5: df_cat के लिए DataFrame तैयार करें
    df_cat = pd.melt(df, id_vars=['cardio'], value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'])

    # Step 6: df_cat को समूहित और पुनः स्वरूपित करें
    df_cat = df_cat.groupby(['cardio', 'variable', 'value']).size().reset_index(name='total')  # कार्डियो के अनुसार डेटा समूहित करें

    # Step 7: लंबा प्रारूप में डेटा परिवर्तित करें और प्लॉट बनाएं
    fig = sns.catplot(x="variable", hue="value", col="cardio", data=df_cat, kind="bar", height=5, aspect=1)

    # Step 8: प्लॉट को सहेजें
    return fig.fig  # प्लॉट का फ़िगर लौटाएँ

# Step 9: अगले दो लाइनों में बदलाव न करें
# draw_cat_plot()

# Step 10: हीट मैप बनाने के लिए फ़ंक्शन बनाएं
def draw_heat_map():
    # Step 11: df_heat को साफ करें
    df_heat = df[
        (df['ap_lo'] <= df['ap_hi']) &  # डाइस्टोलिक प्रेशर को सिस्टोलिक प्रेशर से कम रखें
        (df['height'] >= df['height'].quantile(0.025)) &  # ऊँचाई 2.5 वें पर्सेंटाइल से अधिक हो
        (df['height'] <= df['height'].quantile(0.975)) &  # ऊँचाई 97.5 वें पर्सेंटाइल से कम हो
        (df['weight'] >= df['weight'].quantile(0.025)) &  # वजन 2.5 वें पर्सेंटाइल से अधिक हो
        (df['weight'] <= df['weight'].quantile(0.975))    # वजन 97.5 वें पर्सेंटाइल से कम हो
    ]

    # Step 12: सहसंबंध मैट्रिक्स की गणना करें
    corr = df_heat.corr()  # सहसंबंध मैट्रिक्स की गणना करें

    # Step 13: ऊपरी त्रिकोण के लिए मास्क बनाएँ
    mask = np.triu(np.ones_like(corr, dtype=bool))  # ऊपरी त्रिकोण के लिए मास्क बनाना

    # Step 14: matplotlib चित्र सेट करें
    plt.figure(figsize=(12, 12))

    # Step 15: सहसंबंध मैट्रिक्स को प्लॉट करें
    sns.heatmap(corr, annot=True, mask=mask, fmt='.1f', square=True, cmap="coolwarm", cbar_kws={'shrink': 0.5})

    # Step 16: अगले दो लाइनों में बदलाव न करें
    return plt.gca()  # वर्तमान Axes को लौटाएँ

# यदि आप इसे चलाना चाहते हैं, तो नीचे दिए गए कोड को कमेंट करें
draw_cat_plot()
draw_heat_map()
