from linguonnx import load_detector

# Downloads & caches glotlid-int8 (~419 MB) under ~/.cache/linguonnx/models/ on first use
det = load_detector()  

def detect(text, k=1):
    return next(iter(det.detect_probs(text, top_k=k)))

print(detect("Video bahut badhia heichi.. banei chala!!!"))
# e.g. {'gl': 0.98, 'pt': 0.01, ...}  (macrolanguage-collapsed by default in some configs;
# see below for raw variety-level labels)

# For raw GlotLID variety-level label + confidence (no macrolanguage collapsing):
# print(det.detect_raw("O tempo está moi bo hoxe en Santiago"))
# ('glg_Latn', 0.98...)