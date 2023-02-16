from flask import Flask, render_template, request
from PIL import Image, ImageEnhance
import pytesseract
import re
from decimal import Decimal, ROUND_HALF_UP

app = Flask(__name__)

# Set up Tesseract options
tesseract_config = r'--psm 6 --oem 1'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/bruttonetto', methods=['GET', 'POST'])
def bruttonetto():
    if request.method == 'POST':
        money_value_1 = request.form['money_value_1'].replace(",", ".")
        money_value_2 = request.form['money_value_2'].replace(",", ".")
        money_value_3 = request.form['money_value_3'].replace(",", ".")

        if not money_value_1 or not re.match(r'^\d*\.?\d+$', money_value_1):
            money_value_1 = 0

        if not money_value_2 or not re.match(r'^\d*\.?\d+$', money_value_2):
            money_value_2 = 0

        if not money_value_3 or not re.match(r'^\d*\.?\d+$', money_value_3):
            money_value_3 = 0

        money_value_1 = float(money_value_1)
        money_value_2 = float(money_value_2)
        money_value_3 = float(money_value_3)

        brutto_20 = (money_value_1 * 100) / 120
        brutto_10 = (money_value_2 * 100) / 110
        brutto_13 = (money_value_3 * 100) / 113
        brutto = brutto_20 + brutto_10 + brutto_13
        brutto = Decimal(brutto)
        brutto = brutto.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        return render_template('nettobrutto.html', sum=brutto, money_value_1=money_value_1, money_value_2=money_value_2, money_value_3=money_value_3)
    return render_template('nettobrutto.html', money_value_1=0, money_value_2=0, money_value_3=0)

@app.route('/nettobrutto', methods=['GET', 'POST'])
def nettobrutto():
    if request.method == 'POST':
        money_value_1 = request.form['money_value_1'].replace(",", ".")
        money_value_2 = request.form['money_value_2'].replace(",", ".")
        money_value_3 = request.form['money_value_3'].replace(",", ".")

        if not money_value_1 or not re.match(r'^\d*\.?\d+$', money_value_1):
            money_value_1 = 0

        if not money_value_2 or not re.match(r'^\d*\.?\d+$', money_value_2):
            money_value_2 = 0

        if not money_value_3 or not re.match(r'^\d*\.?\d+$', money_value_3):
            money_value_3 = 0

        money_value_1 = float(money_value_1)
        money_value_2 = float(money_value_2)
        money_value_3 = float(money_value_3)

        netto_20 = money_value_1 * 1.2
        netto_10 = money_value_2 * 1.1
        netto_13 = money_value_3 * 1.13
        netto = netto_20 + netto_10 + netto_13
        netto = Decimal(netto)
        netto = netto.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        return render_template('nettobrutto.html', sum=netto, money_value_1=money_value_1, money_value_2=money_value_2, money_value_3=money_value_3)
    return render_template('nettobrutto.html', money_value_1=0, money_value_2=0, money_value_3=0)


@app.route('/', methods=['POST'])
def upload_image():
    # Get the uploaded image from the form
    image_file = request.files['image']

    # Read the image using PIL
    image = Image.open(image_file).convert('RGBA')
    background = Image.new('RGBA', image.size, (255, 255, 255))

    image = Image.alpha_composite(background, image)

    image = image.transpose(Image.ROTATE_270)

    # Enhance the image
    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(1.5)  # Increase brightness
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(1.5)  # Increase contrast

    image.save("image.png")
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    # Use Tesseract to extract the text from the image
    text = pytesseract.image_to_string(image, config=tesseract_config)

    # Display the extracted text on the webpage
    return render_template('index.html', text=text)


if __name__ == '__main__':
    app.run()
