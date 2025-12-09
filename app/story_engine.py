import random

def generate_story(child_name, age, prompt):
    # Simplu prototip. Va fi înlocuit cu AI real.
    
    templates = [
        f"Într-o zi frumoasă, {child_name} a întâlnit o lumină magică pe nume Kosi. Împreună au început o aventură despre {prompt}.",
        f"{child_name}, un copil curios de {age} ani, a descoperit o poartă secretă către o lume magică. Acolo l-a așteptat Kosi, gata să îi spună povestea despre {prompt}.",
        f"Kosi a apărut ca o mică lumină plutitoare în fața lui {child_name}. \"Hai să-ți spun ceva minunat despre {prompt}\", a spus el."
    ]
    
    return random.choice(templates)
