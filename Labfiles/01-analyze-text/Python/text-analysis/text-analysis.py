from dotenv import load_dotenv
import os

# Import namespaces
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

def main():
    try:
        # Get Configuration Settings
        load_dotenv()
        ai_endpoint = os.getenv('AT_AI_SERVICE_ENDPOINT')
        ai_key = os.getenv('AT_AI_SERVICE_KEY')

        # Create client using endpoint and key
        ai_client = TextAnalyticsClient(
            endpoint=ai_endpoint,
            credential=AzureKeyCredential(ai_key)
        )

        # Analyze each text file in the reviews folder
        reviews_folder = 'reviews/'
        path = os.path.dirname(os.path.abspath(__file__))
        reviews_folder = os.path.join(path, reviews_folder)
        if not os.path.exists(reviews_folder):
            print(f"Reviews folder '{reviews_folder}' does not exist.")
            return
        for file_name in os.listdir(reviews_folder):
            # Read the file contents
            print('\n-------------\n' + file_name)
            text = open(os.path.join(reviews_folder, file_name), encoding='utf8').read()
            print('\n' + text)

            # Get language
            if not text.strip():
                print("No text to analyze.")
                continue
            detectedLanguage = ai_client.detect_language(documents=[text])[0]
            print('\nLanguage: {}'.format(detectedLanguage.primary_language.name))
            print('\nConfidence Score: {}'.format(detectedLanguage.primary_language.confidence_score))

            # Get sentiment
            sentiment = ai_client.analyze_sentiment(documents=[text])[0]
            print('\n'f"Sentiment: {sentiment.sentiment}")
            print('\nPositive Score: {}'.format(sentiment.confidence_scores.positive))
            print('\nNeutral Score: {}'.format(sentiment.confidence_scores.neutral))
            print('\nNegative Score: {}'.format(sentiment.confidence_scores.negative))

            # Get key phrases
            phrases = ai_client.extract_key_phrases(documents=[text])[0]
            if not phrases.key_phrases:
                print('\nNo key phrases found.')
                continue
            print('\nKey Phrases:')
            for phrase in phrases.key_phrases:
                print('\t' + phrase)    

            # Get entities
            entities = ai_client.recognize_entities(documents=[text])[0]
            if not entities.entities:
                print('\nNo entities found.')
                continue
            print('\nEntities:')
            for entity in entities.entities:
                if entity.text:
                    # Print entity text, confidence score, and category
                    print('\t'f"Category Type : {entity.category} ; Text : {entity.text} ; Confidence Score : {entity.confidence_score}")

            # Get linked entities
            linked_entities = ai_client.recognize_linked_entities(documents=[text])[0]
            if not linked_entities.entities:
                print('\nNo linked entities found.')
                continue
            print('\nLinked Entities:')
            for entity in linked_entities.entities:
                if entity.name:
                    # Print linked entity name, data source, and URL
                    print('\t' + f"Name : {entity.name} ; Data Source : {entity.data_source} ; URL : {entity.url}") 


    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()