from transformers import pipeline


model = pipeline(
    "ner",
    model="dslim/bert-base-NER",
    aggregation_strategy="simple"
)


def detect_sensitive_entities(text):

    output = model(text[:3000])

    data = {}


    for i in output:

        label = i["entity_group"]

        word = (
            i["word"]
            .replace("##","")
            .strip()
        )


        if label not in data:

            data[label]=[]


        if word not in data[label]:

            data[label].append(word)


    return data