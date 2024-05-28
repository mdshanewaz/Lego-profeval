# ******************************************************************************
@user_passes_test(test_is_superuser, login_url=reverse_lazy("vug_failed_test", kwargs={'testname': "test_is_superuser", 'viewname': "vdev_testingview"}))
def vdev_testingview(request):
    viewname    = "vdev_testingview"
    zzz_print("    %-28s: %s" % ("viewname START", viewname))

    # Deliberately generating an exception to test
    # mw_viewTracker -> process_view()

    from ..models import mreferral_purchase
    invalid_uniqueid  = "asdfasdf"
    invalid_string_32 = "asdfasdf"
    imreferral_purchase = mreferral_purchase.objects.get(owner_uniqid=invalid_uniqueid, random_string_32=invalid_string_32)
    zzz_print("    %-28s: %s" % ("imreferral_purchase", imreferral_purchase))

    zzz_print("    %-28s: %s" % ("viewname END", viewname))
    return HttpResponseRedirect(reverse('vdev_home'))











































