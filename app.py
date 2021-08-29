from __future__ import division, print_function
# coding=utf-8
import os
import numpy as np

# Keras
from keras.applications.inception_resnet_v2 import preprocess_input
from keras.models import model_from_json
from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator
# from keras.applications.resnet import InceptionResNetV2

# Flask utils
from flask import Flask, redirect, request, render_template
from werkzeug.utils import secure_filename


app = Flask(__name__)

json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("model.h5")
loaded_model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

species_dict = {'AFRICAN CROWNED CRANE': 0,
 'AFRICAN FIREFINCH': 1,
 'ALBATROSS': 2,
 'ALEXANDRINE PARAKEET': 3,
 'AMERICAN AVOCET': 4,
 'AMERICAN BITTERN': 5,
 'AMERICAN COOT': 6,
 'AMERICAN GOLDFINCH': 7,
 'AMERICAN KESTREL': 8,
 'AMERICAN PIPIT': 9,
 'AMERICAN REDSTART': 10,
 'ANHINGA': 11,
 'ANNAS HUMMINGBIRD': 12,
 'ANTBIRD': 13,
 'ARARIPE MANAKIN': 14,
 'ASIAN CRESTED IBIS': 15,
 'BALD EAGLE': 16,
 'BALI STARLING': 17,
 'BALTIMORE ORIOLE': 18,
 'BANANAQUIT': 19,
 'BANDED BROADBILL': 20,
 'BAR-TAILED GODWIT': 21,
 'BARN OWL': 22,
 'BARN SWALLOW': 23,
 'BARRED PUFFBIRD': 24,
 'BAY-BREASTED WARBLER': 25,
 'BEARDED BARBET': 26,
 'BEARDED REEDLING': 27,
 'BELTED KINGFISHER': 28,
 'BIRD OF PARADISE': 29,
 'BLACK & YELLOW bROADBILL': 30,
 'BLACK FRANCOLIN': 31,
 'BLACK SKIMMER': 32,
 'BLACK SWAN': 33,
 'BLACK TAIL CRAKE': 34,
 'BLACK THROATED BUSHTIT': 35,
 'BLACK THROATED WARBLER': 36,
 'BLACK VULTURE': 37,
 'BLACK-CAPPED CHICKADEE': 38,
 'BLACK-NECKED GREBE': 39,
 'BLACK-THROATED SPARROW': 40,
 'BLACKBURNIAM WARBLER': 41,
 'BLUE GROUSE': 42,
 'BLUE HERON': 43,
 'BOBOLINK': 44,
 'BORNEAN BRISTLEHEAD': 45,
 'BORNEAN LEAFBIRD': 46,
 'BROWN NOODY': 47,
 'BROWN THRASHER': 48,
 'BULWERS PHEASANT': 49,
 'CACTUS WREN': 50,
 'CALIFORNIA CONDOR': 51,
 'CALIFORNIA GULL': 52,
 'CALIFORNIA QUAIL': 53,
 'CANARY': 54,
 'CAPE MAY WARBLER': 55,
 'CAPUCHINBIRD': 56,
 'CARMINE BEE-EATER': 57,
 'CASPIAN TERN': 58,
 'CASSOWARY': 59,
 'CEDAR WAXWING': 60,
 'CHARA DE COLLAR': 61,
 'CHIPPING SPARROW': 62,
 'CHUKAR PARTRIDGE': 63,
 'CINNAMON TEAL': 64,
 'CLARKS NUTCRACKER': 65,
 'COCK OF THE  ROCK': 66,
 'COCKATOO': 67,
 'COMMON FIRECREST': 68,
 'COMMON GRACKLE': 69,
 'COMMON HOUSE MARTIN': 70,
 'COMMON LOON': 71,
 'COMMON POORWILL': 72,
 'COMMON STARLING': 73,
 'COUCHS KINGBIRD': 74,
 'CRESTED AUKLET': 75,
 'CRESTED CARACARA': 76,
 'CRESTED NUTHATCH': 77,
 'CROW': 78,
 'CROWNED PIGEON': 79,
 'CUBAN TODY': 80,
 'CURL CRESTED ARACURI': 81,
 'D-ARNAUDS BARBET': 82,
 'DARK EYED JUNCO': 83,
 'DOUBLE BARRED FINCH': 84,
 'DOWNY WOODPECKER': 85,
 'EASTERN BLUEBIRD': 86,
 'EASTERN MEADOWLARK': 87,
 'EASTERN ROSELLA': 88,
 'EASTERN TOWEE': 89,
 'ELEGANT TROGON': 90,
 'ELLIOTS  PHEASANT': 91,
 'EMPEROR PENGUIN': 92,
 'EMU': 93,
 'ENGGANO MYNA': 94,
 'EURASIAN GOLDEN ORIOLE': 95,
 'EURASIAN MAGPIE': 96,
 'EVENING GROSBEAK': 97,
 'FIRE TAILLED MYZORNIS': 98,
 'FLAME TANAGER': 99,
 'FLAMINGO': 100,
 'FRIGATE': 101,
 'GAMBELS QUAIL': 102,
 'GANG GANG COCKATOO': 103,
 'GILA WOODPECKER': 104,
 'GILDED FLICKER': 105,
 'GLOSSY IBIS': 106,
 'GO AWAY BIRD': 107,
 'GOLD WING WARBLER': 108,
 'GOLDEN CHEEKED WARBLER': 109,
 'GOLDEN CHLOROPHONIA': 110,
 'GOLDEN EAGLE': 111,
 'GOLDEN PHEASANT': 112,
 'GOLDEN PIPIT': 113,
 'GOULDIAN FINCH': 114,
 'GRAY CATBIRD': 115,
 'GRAY PARTRIDGE': 116,
 'GREAT POTOO': 117,
 'GREATOR SAGE GROUSE': 118,
 'GREEN JAY': 119,
 'GREEN MAGPIE': 120,
 'GREY PLOVER': 121,
 'GUINEA TURACO': 122,
 'GUINEAFOWL': 123,
 'GYRFALCON': 124,
 'HARPY EAGLE': 125,
 'HAWAIIAN GOOSE': 126,
 'HELMET VANGA': 127,
 'HIMALAYAN MONAL': 128,
 'HOATZIN': 129,
 'HOODED MERGANSER': 130,
 'HOOPOES': 131,
 'HORNBILL': 132,
 'HORNED GUAN': 133,
 'HORNED SUNGEM': 134,
 'HOUSE FINCH': 135,
 'HOUSE SPARROW': 136,
 'IMPERIAL SHAQ': 137,
 'INCA TERN': 138,
 'INDIAN BUSTARD': 139,
 'INDIAN PITTA': 140,
 'INDIGO BUNTING': 141,
 'JABIRU': 142,
 'JAVA SPARROW': 143,
 'KAKAPO': 144,
 'KILLDEAR': 145,
 'KING VULTURE': 146,
 'KIWI': 147,
 'KOOKABURRA': 148,
 'LARK BUNTING': 149,
 'LEARS MACAW': 150,
 'LILAC ROLLER': 151,
 'LONG-EARED OWL': 152,
 'MAGPIE GOOSE': 153,
 'MALABAR HORNBILL': 154,
 'MALACHITE KINGFISHER': 155,
 'MALEO': 156,
 'MALLARD DUCK': 157,
 'MANDRIN DUCK': 158,
 'MARABOU STORK': 159,
 'MASKED BOOBY': 160,
 'MASKED LAPWING': 161,
 'MIKADO  PHEASANT': 162,
 'MOURNING DOVE': 163,
 'MYNA': 164,
 'NICOBAR PIGEON': 165,
 'NOISY FRIARBIRD': 166,
 'NORTHERN BALD IBIS': 167,
 'NORTHERN CARDINAL': 168,
 'NORTHERN FLICKER': 169,
 'NORTHERN GANNET': 170,
 'NORTHERN GOSHAWK': 171,
 'NORTHERN JACANA': 172,
 'NORTHERN MOCKINGBIRD': 173,
 'NORTHERN PARULA': 174,
 'NORTHERN RED BISHOP': 175,
 'NORTHERN SHOVELER': 176,
 'OCELLATED TURKEY': 177,
 'OKINAWA RAIL': 178,
 'OSPREY': 179,
 'OSTRICH': 180,
 'OVENBIRD': 181,
 'OYSTER CATCHER': 182,
 'PAINTED BUNTIG': 183,
 'PALILA': 184,
 'PARADISE TANAGER': 185,
 'PARAKETT  AKULET': 186,
 'PARUS MAJOR': 187,
 'PEACOCK': 188,
 'PELICAN': 189,
 'PEREGRINE FALCON': 190,
 'PHILIPPINE EAGLE': 191,
 'PINK ROBIN': 192,
 'PUFFIN': 193,
 'PURPLE FINCH': 194,
 'PURPLE GALLINULE': 195,
 'PURPLE MARTIN': 196,
 'PURPLE SWAMPHEN': 197,
 'PYGMY KINGFISHER': 198,
 'QUETZAL': 199,
 'RAINBOW LORIKEET': 200,
 'RAZORBILL': 201,
 'RED BEARDED BEE EATER': 202,
 'RED BELLIED PITTA': 203,
 'RED BROWED FINCH': 204,
 'RED FACED CORMORANT': 205,
 'RED FACED WARBLER': 206,
 'RED HEADED DUCK': 207,
 'RED HEADED WOODPECKER': 208,
 'RED HONEY CREEPER': 209,
 'RED TAILED THRUSH': 210,
 'RED WINGED BLACKBIRD': 211,
 'RED WISKERED BULBUL': 212,
 'REGENT BOWERBIRD': 213,
 'RING-NECKED PHEASANT': 214,
 'ROADRUNNER': 215,
 'ROBIN': 216,
 'ROCK DOVE': 217,
 'ROSY FACED LOVEBIRD': 218,
 'ROUGH LEG BUZZARD': 219,
 'ROYAL FLYCATCHER': 220,
 'RUBY THROATED HUMMINGBIRD': 221,
 'RUFOUS KINGFISHER': 222,
 'RUFUOS MOTMOT': 223,
 'SAMATRAN THRUSH': 224,
 'SAND MARTIN': 225,
 'SCARLET IBIS': 226,
 'SCARLET MACAW': 227,
 'SHOEBILL': 228,
 'SHORT BILLED DOWITCHER': 229,
 'SMITHS LONGSPUR': 230,
 'SNOWY EGRET': 231,
 'SNOWY OWL': 232,
 'SORA': 233,
 'SPANGLED COTINGA': 234,
 'SPLENDID WREN': 235,
 'SPOON BILED SANDPIPER': 236,
 'SPOONBILL': 237,
 'SRI LANKA BLUE MAGPIE': 238,
 'STEAMER DUCK': 239,
 'STORK BILLED KINGFISHER': 240,
 'STRAWBERRY FINCH': 241,
 'STRIPPED SWALLOW': 242,
 'SUPERB STARLING': 243,
 'SWINHOES PHEASANT': 244,
 'TAIWAN MAGPIE': 245,
 'TAKAHE': 246,
 'TASMANIAN HEN': 247,
 'TEAL DUCK': 248,
 'TIT MOUSE': 249,
 'TOUCHAN': 250,
 'TOWNSENDS WARBLER': 251,
 'TREE SWALLOW': 252,
 'TRUMPTER SWAN': 253,
 'TURKEY VULTURE': 254,
 'TURQUOISE MOTMOT': 255,
 'UMBRELLA BIRD': 256,
 'VARIED THRUSH': 257,
 'VENEZUELIAN TROUPIAL': 258,
 'VERMILION FLYCATHER': 259,
 'VICTORIA CROWNED PIGEON': 260,
 'VIOLET GREEN SWALLOW': 261,
 'VULTURINE GUINEAFOWL': 262,
 'WATTLED CURASSOW': 263,
 'WHIMBREL': 264,
 'WHITE CHEEKED TURACO': 265,
 'WHITE NECKED RAVEN': 266,
 'WHITE TAILED TROPIC': 267,
 'WHITE THROATED BEE EATER': 268,
 'WILD TURKEY': 269,
 'WILSONS BIRD OF PARADISE': 270,
 'WOOD DUCK': 271,
 'YELLOW BELLIED FLOWERPECKER': 272,
 'YELLOW CACIQUE': 273,
 'YELLOW HEADED BLACKBIRD': 274}

key_list = list(species_dict.keys())



def model_predict(img_path, model):
    
    
    img = image.load_img(img_path, target_size=(224, 224))

    # Preprocessing the image
    x = image.img_to_array(img)
    #x = np.true_divide(img, 255)
    x = np.expand_dims(x, axis=0)
    

    # Be careful how your trained model deals with the input
    # otherwise, it won't make correct prediction!
    # x = preprocess_input(x, mode='caffe')
    
    x = preprocess_input(x)

    preds = loaded_model.predict(x)
    return preds



@app.route('/',methods=['GET'])


def Home():
    return render_template('index.html')

@app.route("/upload-image", methods=['GET','POST'])

def upload_image():
    
    if request.method == 'POST':
        
        if request.files:
        
            ## check if the post request has the file part
            image = request.files['image']
            
            # Save the file to ./uploads
            basepath = os.path.dirname(__file__)
            file_path = os.path.join(
                basepath, 'uploads', secure_filename(image.filename))
            image.save(file_path)
    
            # Make prediction
            preds = model_predict(file_path, loaded_model)
    
            # Process your result for human
            pred_class = preds.argmax(axis=-1)            # Simple argmax
            # pred_class = decode_predictions(preds, top=1)   # ImageNet Decode
            # result = str(pred_class[0][0][1])               # Convert to string
            result = key_list[int(pred_class)]
            
            # return redirect(request.url)

            return render_template('result.html', prediction = result)
                        
    else:
        
        return render_template('index.html')

if __name__=="__main__":
    
    app.run(debug=True)

