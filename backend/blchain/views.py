from django.http import HttpResponse, JsonResponse
import subprocess, os
import json
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view


def blchain(match_score):
    original_directory = os.getcwd()

    print("original path", original_directory)

    try:
        os.chdir('blchain/truffle')

        process = subprocess.Popen(['truffle', 'exec', 'add_match.js', '--network', 'development', '--args', str(match_score)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()

        if error:
            error_message = error.decode('utf-8')
            return HttpResponse(f"Error: {error_message}", status=500)
        else:
            output_message = output.decode('utf-8')
            return HttpResponse(output_message, status=200)
    except Exception as e:
        return HttpResponse(f"Exception: {str(e)}", status=500)
    finally:
        os.chdir(original_directory)

@csrf_exempt
@api_view(['POST'])
def blchain_add_data(request):

    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    if not request.body:
        return JsonResponse({'error': 'empty body'}, status=400)

    try:
        data = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Error al decodificar el JSON'}, status=400)

    if 'match_score' not in data:
        return JsonResponse({'error': 'Falta la clave match_score en el JSON'}, status=400)

    match_score = data['match_score']

    return blchain(match_score)

@api_view(['GET'])
def blchain_get_data(request):

    original_directory = os.getcwd()

    try:
        os.chdir('blchain/truffle')
 
        process = subprocess.Popen(['truffle', 'exec', 'get_matchs.js', '--network', 'development'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()

        if error:
            print("Error:", error.decode('utf-8'))
        else:
            output_str = output.decode('utf-8')
            cleaned = dataPreparation(output_str)
            jsonOutput = json.dumps(cleaned, indent=4)
            return HttpResponse(jsonOutput)

    except Exception as e:
        return HttpResponse(f"Exception: {str(e)}", status=500)
    finally:
        os.chdir(original_directory)


def dataPreparation(output):
    
    text_to_replace = "Using network 'development'.\n\n"

    cleaned_str = output.replace(text_to_replace, "")

    lines = cleaned_str.split("\n")
    lines = cleaned_str.strip().splitlines()


    dataJson = []
    

    for line in lines:
        pairs = line.split(" ")

        dataDict = {}
        for pair in pairs:
            if '=' in pair:
                (key, value) = pair.split('=')
                dataDict[key] = value
        dataJson.append(dataDict)

   
    return(dataJson)
