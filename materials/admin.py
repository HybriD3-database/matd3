from django.contrib import admin

from materials.models import (
    Tag, System, AtomicPositions, Publication, Author, Phase, ExcitonEmission,
    SynthesisMethod, BandStructure, Method, SpecificMethod, PropertyOld,
    MaterialProperty)

admin.site.register(System)
admin.site.register(AtomicPositions)
admin.site.register(Publication)
admin.site.register(Author)
admin.site.register(Phase)
admin.site.register(ExcitonEmission)
admin.site.register(SynthesisMethod)
admin.site.register(BandStructure)
admin.site.register(Tag)
admin.site.register(Method)
admin.site.register(SpecificMethod)
admin.site.register(PropertyOld)
admin.site.register(MaterialProperty)
