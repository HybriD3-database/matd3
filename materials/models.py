# -*- coding: utf-8 -*-
import os
import shutil

from django.db import models
from mainproject import settings


def file_name(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s_%s_%s_apos.%s" % (instance.phase, instance.system.organic,
                                     instance.system.inorganic, ext)
    return os.path.join('uploads', filename)


def pl_file_name(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s_%s_%s_pl.%s" % (instance.phase, instance.system.organic,
                                   instance.system.inorganic, ext)
    return os.path.join('uploads', filename)


def syn_file_name(instance, filename):
    filename = "%s_%s_%s_syn.txt" % (instance.phase, instance.system.organic,
                                     instance.system.inorganic)
    return os.path.join('uploads', filename)


class Post(models.Model):
    """Create your models here."""
    post = models.CharField(max_length=500)


class Publication(models.Model):
    author_count = models.PositiveSmallIntegerField()
    title = models.CharField(max_length=1000)
    journal = models.CharField(max_length=500, blank=True)
    vol = models.CharField(max_length=100)
    pages_start = models.CharField(max_length=10)
    pages_end = models.CharField(max_length=10)
    year = models.CharField(max_length=4)
    doi_isbn = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.title

    def getAuthors(self):
        return self.author_set.all()


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    institution = models.CharField(max_length=100, blank=True)
    publication = models.ManyToManyField(Publication)

    def __str__(self):
        value = (self.first_name + " " + self.last_name + ", " +
                 self.institution)
        if len(value) > 45:
            value = value[:42] + '...'
        return value

    def splitFirstName(self):
        return self.first_name.split()


class Tag(models.Model):
    tag = models.CharField(max_length=100)

    def __str__(self):
        return self.tag


class System(models.Model):
    """Contains meta data for investigated system. """
    compound_name = models.CharField(max_length=1000)
    formula = models.CharField(max_length=200)
    group = models.CharField(max_length=100)  # aka Alternate names
    organic = models.CharField(max_length=100)
    inorganic = models.CharField(max_length=100)
    last_update = models.DateField(auto_now=True)
    description = models.TextField(max_length=1000, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.compound_name

    def listAlternateNames(self):
        return self.group.replace(',', ' ').split()

    def listProperties(self):
        L = []
        for mat_prop in self.materialproperty_set.all():
            property = mat_prop.property
            if property not in L:
                L.append(property)
        return L

    def getAuthors(self):
        """Returns a list of authors related to a system

        an author appears no more than once

        """
        def authorSort(author):  # function that decides author sort criteria
            return author.last_name

        L = []
        for dataType in [self.atomicpositions_set, self.synthesismethod_set,
                         self.excitonemission_set, self.bandstructure_set]:
            for data in dataType.all():
                for author in data.publication.author_set.all():
                    if author not in L:  # don't add duplicate authors
                        L.append(author)

        return sorted(L, key=authorSort)

    # This type of function can be used to display numbers as subscripts in
    # chemical formulas. Simply create functions of this type for each field
    # that would need subscripts, then call it from the template e.g.
    # {{system.compoundNameFormat|safe}}. The |safe allows the string to be
    # rendered as html, but has potential security issues if someone were to
    # enter html into a form field (such as compound_name). This also has the
    # problem of turning every number into a subscript, even ones that are part
    # of an abbreviation (e.g. AE4TPbI4).
    '''
    def compoundNameFormat(self):
        formattedString = ''
        for c in self.compound_name:
            if c.isdigit():
                formattedString += '<sub>' + c + '</sub>'
            else:
                formattedString += c
        return formattedString
    '''


class Phase(models.Model):
    phase = models.CharField(max_length=50)

    def __str__(self):
        return self.phase


class Method(models.Model):
    method = models.CharField(max_length=100)

    def __str__(self):
        return self.method


class SpecificMethod(models.Model):
    specific_method = models.CharField(max_length=500)

    def __str__(self):
        return self.specific_method


class PropertyOld(models.Model):
    property = models.CharField(max_length=500)

    class Meta:
        verbose_name_plural = "properties"

    def __str__(self):
        return self.property


class IDInfo(models.Model):
    publication = models.ForeignKey(Publication, on_delete=models.PROTECT)
    source = models.CharField(max_length=500)
    data_extraction_method = models.CharField(max_length=500)
    contributor = models.ForeignKey('accounts.UserProfile',
                                    on_delete=models.PROTECT)
    temperature = models.CharField(max_length=20, blank=True)
    phase = models.ForeignKey(Phase, on_delete=models.PROTECT)
    method = models.ForeignKey(Method, on_delete=models.PROTECT, null=True)
    specific_method = models.ForeignKey(SpecificMethod,
                                        on_delete=models.PROTECT, null=True)
    comments = models.CharField(max_length=1000, blank=True)
    last_update = models.DateField(auto_now=True)

    def getAuthors(self):
        return self.publication.getAuthors()


class SynthesisMethod(IDInfo):
    system = models.ForeignKey(System, on_delete=models.PROTECT)
    synthesis_method = models.TextField(max_length=1000, blank=True)
    starting_materials = models.TextField(max_length=1000, blank=True)
    remarks = models.TextField(max_length=1000, blank=True)
    product = models.TextField(max_length=1000, blank=True)
    syn_file = models.FileField(upload_to=syn_file_name, blank=True)

    def __str__(self):
        return (self.system.compound_name + " synthesis #" +
                str(self.methodNumber()))

    def methodNumber(self):
        for i, obj in enumerate(self.system.synthesismethod_set.all()):
            if obj.pk == self.pk:
                return i + 1


class ExcitonEmission(IDInfo):
    system = models.ForeignKey(System, on_delete=models.PROTECT)
    exciton_emission = models.DecimalField(max_digits=7, decimal_places=4)
    pl_file = models.FileField(upload_to=pl_file_name, blank=True)
    plotted = models.BooleanField(default=False)
    synthesis_method = models.ForeignKey(SynthesisMethod,
                                         on_delete=models.PROTECT, null=True,
                                         blank=True)

    def __str__(self):
        return str(self.exciton_emission)


class BandStructure(IDInfo):
    system = models.ForeignKey(System, on_delete=models.PROTECT)
    band_gap = models.CharField(max_length=10, blank=True)
    folder_location = models.CharField(max_length=500, blank=True)
    plotted = models.BooleanField(default=False)
    visible = models.BooleanField(default=False)
    synthesis_method = models.ForeignKey(SynthesisMethod,
                                         on_delete=models.PROTECT, null=True,
                                         blank=True)

    def __str__(self):
        return self.folder_location

    def getFullBSPath(self):
        path = (
            "../../media/uploads/%s_%s_%s_%s_bs/%s_%s_%s_%s_bs_full.png" %
            (self.phase, self.system.organic, self.system.inorganic, self.pk,
             self.phase, self.system.organic, self.system.inorganic, self.pk))
        return path

    def getMiniBSPath(self):
        path = (
            "../../media/uploads/%s_%s_%s_%s_bs/%s_%s_%s_%s_bs_min.png" %
            (self.phase, self.system.organic, self.system.inorganic, self.pk,
             self.phase, self.system.organic, self.system.inorganic, self.pk))
        return path


class AtomicPositions(IDInfo):
    system = models.ForeignKey(System, on_delete=models.PROTECT)
    a = models.CharField(max_length=50)
    b = models.CharField(max_length=50)
    c = models.CharField(max_length=50)
    alpha = models.CharField(max_length=50)
    beta = models.CharField(max_length=50)
    gamma = models.CharField(max_length=50)
    volume = models.CharField(max_length=50, blank=True)
    Z = models.CharField(max_length=50, blank=True)
    fhi_file = models.FileField(upload_to=file_name, blank=True)
    synthesis_method = models.ForeignKey(SynthesisMethod,
                                         on_delete=models.PROTECT, null=True,
                                         blank=True)

    class Meta:
        verbose_name_plural = "atomic positions"

    def __str__(self):
        return self.phase.phase + " " + self.system.formula


class MaterialProperty(IDInfo):
    system = models.ForeignKey(System, on_delete=models.PROTECT)
    property = models.ForeignKey(PropertyOld, on_delete=models.PROTECT)
    value = models.CharField(max_length=500)

    class Meta:
        verbose_name_plural = "material properties"

    def __str__(self):
        return str(self.system) + ' ' + str(self.property) + ': ' + self.value


class BondAngle(IDInfo):
    system = models.ForeignKey(System, on_delete=models.PROTECT)
    hmh_angle = models.CharField(max_length=100, blank=True)
    mhm_angle = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.hmh_angle + " " + self.mhm_angle


class BondLength(IDInfo):
    system = models.ForeignKey(System, on_delete=models.PROTECT)
    hmh_length = models.CharField(max_length=100, blank=True)
    mhm_length = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.hmh_length + " " + self.mhm_length


def del_bs(sender, instance, **kwargs):
    folder_loc = instance.folder_location
    if os.path.isdir(folder_loc):
        shutil.rmtree(folder_loc)


def del_pl(sender, instance, **kwargs):
    if(instance.pl_file):
        file_loc = (settings.MEDIA_ROOT + "/uploads/" +
                    str(instance.pl_file).split("/")[1])
        if os.path.isfile(file_loc):
            os.remove(file_loc)


def del_apos(sender, instance, **kwargs):
    if(instance.fhi_file):
        file_loc = (settings.MEDIA_ROOT + "/uploads/" +
                    str(instance.fhi_file).split("/")[1])
        if os.path.isfile(file_loc):
            os.remove(file_loc)


models.signals.post_delete.connect(del_bs, sender=BandStructure)
models.signals.post_delete.connect(del_pl, sender=ExcitonEmission)
models.signals.post_delete.connect(del_apos, sender=AtomicPositions)
