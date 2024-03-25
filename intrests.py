data = [
    {
        "name": "Information Technology",
        "description" : "all about computer sience and technology",
        "intrests": [
            {
                "name": "Python",
                "description": "Python is an interpreted, high-level and general-purpose programming language. Python's design philosophy emphasizes code readability with its notable use of significant whitespace.",
            },
            {
                "name": "Linear Algebra",
                "description": "Linear algebra is the branch of mathematics concerning linear equations such as linear functions such as and their representations through matrices and vector spaces.",
            },
            {
                "name": "Calculus",
                "description": "Calculus is the mathematical study of continuous change, in the same way that geometry is the study of shape and algebra is the study of generalizations of arithmetic operations.",
            }
        ]
    },
    {
        "name": "Business",
        "description" : "all about business",
        "intrests": [
            {
                "name": "Marketing",
                "description": "Marketing refers to activities a company undertakes to promote the buying or selling of a product or service. Marketing includes advertising, selling, and delivering products to consumers or other businesses.",
            },
            {
                "name": "Finance",
                "description": "Finance is a term for matters regarding the management, creation, and study of money and investments. Finance can be broadly divided into three categories, public finance, corporate finance, and personal finance.",
            },
            {
                "name": "Accounting",
                "description": "Accounting is the process of recording financial transactions pertaining to a business. The accounting process includes summarizing, analyzing and reporting these transactions to oversight agencies, regulators and tax collection entities.",
            }
        ]
    },
    {
        "name": "Mathematics",
        "description" : "all about mathematics",
        "intrests": [
            {
                "name": "Algebra",
                "description": "Algebra is one of the broad parts of mathematics, together with number theory, geometry and analysis. In its most general form, algebra is the study of mathematical symbols and the rules for manipulating these symbols; it is a unifying thread of almost all of mathematics.",
            },
            {
                "name": "Geometry",
                "description": "Geometry is a branch of mathematics concerned with questions of shape, size, relative position of figures, and the properties of space.",
            },
            {
                "name": "Trigonometry",
                "description": "Trigonometry is a branch of mathematics that studies relationships between side lengths and angles of triangles. The field emerged in the Hellenistic world during the 3rd century BC from applications of geometry to astronomical studies.",
            }
        ]
    },
    {
        "name": "Physics",
        "description": "Physics is the natural science that studies matter, its motion and behavior through space and time, and the related entities of energy and force. Physics is one of the most fundamental scientific disciplines, and its main goal is to understand how the universe behaves.",
        "intrests": [
            {
                "name": "Mechanics",
                "description": "Mechanics is the branch of physics concerned with the behavior of physical bodies when subjected to forces or displacements, and the subsequent effects of the bodies on their environment.",
            },
            {
                "name": "Thermodynamics",
                "description": "Thermodynamics is a branch of physics that deals with heat, work, and temperature, and their relation to energy, radiation, and physical properties of matter.",
            },
            {
                "name": "Electromagnetism",
                "description": "Electromagnetism is a branch of physics involving the study of the electromagnetic force, a type of physical interaction that occurs between electrically charged particles.",
            }
        ]
    },
    {
        "name": "Chemistry",
        "description": "Chemistry is the scientific discipline involved with elements and compounds composed of atoms, molecules and ions: their composition, structure, properties, behavior and the changes they undergo during a reaction with other substances.",
        "intrests": [
            {
                "name": "Organic Chemistry",
                "description": "Organic chemistry is a subdiscipline of chemistry that studies the structure, properties and reactions of organic compounds, which contain carbon in covalent bonding.",
            },
            {
                "name": "Inorganic Chemistry",
                "description": "Inorganic chemistry deals with the synthesis and behavior of inorganic and organometallic compounds. This field covers all chemical compounds except the myriad organic compounds, which are the subjects of organic chemistry.",
            },
            {
                "name": "Chemical Equations",
                "description": "A chemical equation is the symbolic representation of a chemical reaction in the form of symbols and formulae, wherein the reactant entities are given on the left-hand side and the product entities on the right-hand side.",
            }
        ]
    },
    {
        "name": "Biology",
        "description": "Biology is the natural science that studies life and living organisms, including their physical structure, chemical processes, molecular interactions, physiological mechanisms, development and evolution.",
        "intrests": [
            {
                "name": "Cell Biology",
                "description": "Cell biology is a branch of biology studying the structure and function of the cell, also known as the basic unit of life.",
            },
            {
                "name": "Genetics",
                "description": "Genetics is a branch of biology concerned with the study of genes, genetic variation, and heredity in organisms.",
            },{
                "name": "Evolution",
                "description": "Evolution is change in the heritable characteristics of biological populations over successive generations.",
            }
        ]
    }
]

# from intrest.models import Category, Interest

# def populate():
#     for category in data:
#         try:
#             Category.objects.get(name=category["name"])
#             pass
        
#         except Category.DoesNotExist:
#             category_obj = Category.objects.create(name=category["name"], description=category["description"])
#             for intrest in category["intrests"]:
#                 Interest.objects.create(name=intrest["name"], description=intrest["description"], category=category_obj)

#     return True

import requests
