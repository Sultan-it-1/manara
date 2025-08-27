from flask import Flask, request, jsonify, send_file
from PIL import Image, ImageDraw, ImageFont
import io

app = Flask(__name__)

def add_watermark(img, watermark_text="© Sultan"):
    # إنشاء صورة شفافة لنقش العلامة المائية
    watermark = Image.new("RGBA", img.size)
    draw = ImageDraw.Draw(watermark)

    # إعداد الخط
    try:
        font_size = max(20, img.size[0] // 20)
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()

    # حساب حجم النص باستخدام Pillow 10+
    bbox = draw.textbbox((0, 0), watermark_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # وضع النص في أسفل يمين الصورة
    x = img.size[0] - text_width - 10
    y = img.size[1] - text_height - 10
    draw.text((x, y), watermark_text, font=font, fill=(255, 255, 255, 128))

    # دمج العلامة المائية مع الصورة الأصلية
    return Image.alpha_composite(img.convert("RGBA"), watermark).convert("RGB")

@app.route("/process", methods=["POST"])
def process_image():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400

        file = request.files['file']
        img = Image.open(file.stream)

        # أضف watermark
        processed_img = add_watermark(img)

        # حفظ الصورة في ذاكرة لإرسالها كرد
        output = io.BytesIO()
        processed_img.save(output, format="JPEG")
        output.seek(0)

        return send_file(output, mimetype='image/jpeg')

    except Exception as e:
        # أي خطأ داخلي يرجع رسالة واضحة بدل 500
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
