import cohere
from cohere.responses.classify import Example
from src.llm_agents.translators.cohere_translator import CohereTranslator
from src.llm_agents.constants import COHERE_API_KEY

import time

translator = CohereTranslator()

co = cohere.Client(COHERE_API_KEY)
# examples=[
#   Example("اكتشف فريق بحثي بقيادة علماء فلك من جامعة هارفارد أبعد ثقب أسود فائق الكتلة شوهد حتى الآن، حيث نشأ حينما كان عمر الكون نحو 470 مليون سنة بعد الانفجار العظيم، مع كتلة هائلة تظل إلى الآن لغزا كبيرا.", "لا يحتوي على تعريف لمصطلح"),
#   Example('والثقب الأسود فائق الكتلة هو أكبر نوع من الثقوب السوداء، حيث تبلغ كتلته مئات الآلاف أو ملايين إلى مليارات أضعاف كتلة الشمس، وتشير الأدلة الرصدية إلى أن كل مجرة كبيرة تقريبا تحتوي على ثقب أسود فائق في مركزها. وعلى سبيل المثال، تحتوي مجرة درب التبانة على ثقب أسود فائق في مركزها يسمى الرامي أ*.', "يحتوي على تعريف لمصطلح"),
#   Example('مع ارتفاع حرارة كوكب الأرض، ستواجه الأنواع الحيوانية والنباتية في جميع أنحاء العالم ظروفا معيشية جديدة لا يمكن التنبؤ بها، مما قد يغير النظم البيئية بطرق غير مسبوقة.', "لا يحتوي على تعريف لمصطلح"),
#   Example('والبولي إيثيلين تيريفثاليت، مادة بلاستيكية حرارية تستخدم في جميع الصناعات الكيميائية الحديثة، ويتجاوز الطلب العالمي على هذه المادة نحو 30 مليون طن سنويا، ويصَمم أكثر من 80% منها للاستخدام مرة واحدة، مما يؤدي إلى 25 مليون طن سنويا من النفايات، ويساهم في أزمة نفايات عالمية، كما يقول الباحثون في مقدمة دراستهم.', "يحتوي على تعريف لمصطلح"),
#   Example('وعلى الرغم من وجود أساليب كيميائية وميكانيكية راسخة لإعادة تدوير تلك النفايات، فإن تللك الأساليب ليست صديقة للبيئة بدرجة كافية. وفي المقابل فإن تقنيات إعادة التدوير الحيوي، المعتمِدة على العمليات الأنزيمية والكائنات الحية الدقيقة التي تعالج تلك المشكلة، لا تزال أقل رسوخا، وذلك بسبب عراقيل يزعم الباحثون أنهم نجحوا في تجاوزها خلال تلك الدراسة.', "لا يحتوي على تعريف لمصطلح"),
#   Example('وخلال العام الماضي، أظهر فريق في الولايات المتحدة أنه من الممكن زراعة النباتات في القمر عن طريق زراعة عدد صغير من الأعشاب الضارة تسمى رشاد الثال في عينات التربة القمرية الحقيقية. وأظهر هذا الاختبار أن التربة القمرية يمكن أن تكون فعالة، ولكنها ليست جيدة بما يكفي لنضج النباتات وإنتاج الغذاء.', "لا يحتوي على تعريف لمصطلح"),
# ]

examples = [
    Example(
        "Artificial intelligence (AI) refers to the development of computer systems able to perform tasks that typically require human intelligence, such as visual perception, speech recognition, decision-making, and language translation.",
        "Contains a definition of a term"),
    Example(
        "The Internet of Things (IoT) describes the network of physical devices, vehicles, home appliances, and other items embedded with sensors, software, and connectivity, allowing these objects to collect and exchange data.",
        "Contains a definition of a term"),
    Example(
        "Blockchain is a decentralized digital ledger that records transactions across multiple computers in a secure and transparent manner, enabling trustless and tamper-proof data management.",
        "Contains a definition of a term"),
    Example(
        "Meanwhile, Mars and Earth are now orbiting on the opposite sides of the sun, temporarily disrupting communications between NASA and its robotic explorers investigating the red planet.",
        "Does not contain a definition of a term"),
    Example(
        "We are ready to continue our cooperation with the United States on panda conservation, and do our best to meet the wishes of the Californians so as to deepen the friendly ties between our two peoples.",
        "Does not contain a definition of a term"),
    Example(
        "Rishi Sunak becoming Britain's prime minister is a “Barak Obama moment” for people of Indian descent in the UK, the president of the Hindu temple in the UK co-founded by Sunak’s grandparents in 1971 told CNN.  ",
        "Does not contain a definition of a term"),
]

# inputs=[
#     'يقول غرويف في البيان الصحفي المنشور على موقع الجامعة "لقد استوحينا الإلهام من النظام البصري للفراشات القادرة على إدراك مناطق متعددة في طيف الأشعة فوق البنفسجية، وقمنا بتصميم كاميرا تحاكي هذه الوظيفة. وقد فعلنا ذلك باستخدام بلورات البيروفسكايت النانوية الجديدة جنبا إلى جنب مع تكنولوجيا التصوير السيليكونية، ويمكن لتقنية الكاميرا الجديدة هذه اكتشاف مناطق متعددة للأشعة فوق البنفسجية".',
#     'والضوء فوق البنفسجي هو إشعاع كهرومغناطيسي ذو أطوال موجية أقصر من الضوء المرئي، ولكنه أطول من الأشعة السينية. ويتم تصنيف ضوء الأشعة فوق البنفسجية إلى 3 نطاقات بناء على الأطوال الموجية المختلفة. ونظرا لأن البشر لا يستطيعون رؤية الأشعة فوق البنفسجية، فمن الصعب التقاط معلومات الأشعة فوق البنفسجية، أو التمييز بين الاختلافات الصغيرة لكل نطاق.',
#     'ومع ذلك تستطيع الفراشات رؤية هذه الاختلافات الصغيرة في طيف الأشعة فوق البنفسجية، مثلما يستطيع البشر رؤية ظلال اللون الأزرق والأخضر.',
#     'وبلورات البيروفسكايت النانوية هي فئة من البلورات النانوية شبه الموصلة التي تقدم خصائص فريدة مشابهة لتلك الموجودة في النقاط الكمومية، حيث يؤدي تغيير حجم وتكوين الجسيمات إلى تغيير خصائص الامتصاص والانبعاث للمادة. وفي السنوات القليلة الماضية، ظهرت بلورات البيروفسكايت النانوية كمواد مثيرة للاهتمام لتطبيقات الاستشعار المختلفة، مثل الخلايا الشمسية ومصابيح الليد.',
# ]


def classify_definition(paragraph):
    paragraph = translator.extract(paragraph)
    print("\nTRANSLATED", paragraph)
    while True:
        try:
            response = co.classify(
                model="embed-multilingual-v2.0",
                inputs=[paragraph],
                examples=examples,
            )
            break
        except cohere.error.CohereAPIError as e:
            time.sleep(10)

    response = response[0]
    print("\RESPONSE", response)

    if response.predictions[0] == "Does not contain a definition of a term":
        return False
    else:
        return True