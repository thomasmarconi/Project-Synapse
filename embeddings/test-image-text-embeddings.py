"""This script demonstrates how to use the CLIP model to encode images and text."""

from PIL import Image
import clip
import torch

print("🚀 Welcome to the CLIP Model Demo! 🚀")
print("📋 This script will encode an image and text using OpenAI's CLIP model")
print("=" * 60)

print("\n🔧 Step 1: Loading the CLIP model...")
print("   Loading ViT-B/32 architecture from OpenAI...")
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
print(f"   🎯 Using device: {DEVICE}")
if DEVICE == "cuda":
    print(f"   🚀 GPU detected: {torch.cuda.get_device_name(0)}")
    print(
        f"   💾 GPU memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB"
    )
else:
    print("   ⚠️  No CUDA available, falling back to CPU")
model, preprocess = clip.load("ViT-B/32", device=DEVICE)
print("   ✅ Model loaded successfully!")

print("\n🖼️  Step 2: Processing the image...")
print("   Opening and preprocessing 'boom.png'...")
image = preprocess(Image.open("boom.png")).unsqueeze(0).to(DEVICE)
print(f"   📍 Image moved to {DEVICE}")
print("   ✅ Image loaded and preprocessed!")

print("\n📝 Step 3: Tokenizing text descriptions...")
print("   Tokenizing: ['a photo of a cat', 'a dog', 'a car']")
text = clip.tokenize(["a photo of a cat", "a dog", "a car"]).to(DEVICE)
print(f"   📍 Text tokens moved to {DEVICE}")
print("   ✅ Text successfully tokenized!")

print("\n🧠 Step 4: Encoding features (no gradients)...")
print("   Entering inference mode (torch.no_grad)...")
with torch.no_grad():
    print("   🔄 Encoding image into feature vector...")
    image_features = model.encode_image(image)
    print("   🔄 Encoding text into feature vectors...")
    text_features = model.encode_text(text)

print("   ✅ Feature encoding complete!")

print("\n" + "=" * 60)
print("📊 RESULTS:")
print("=" * 60)
print(f"🖼️  Image features shape: {image_features.shape}")
print(f"📝 Text features shape:  {text_features.shape}")
print(f"🎯 Image features device: {image_features.device}")
print(f"🎯 Text features device:  {text_features.device}")

print("\n📈 Raw Features (first 5 dimensions):")
print(f"   Image: {image_features[0, :5].tolist()}")
print(f"   Text:  {text_features[0, :5].tolist()}")

print("\n🎉 Demo complete! Your image and text have been successfully encoded! 🎉")
