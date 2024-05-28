# ******************************************************************************
@user_passes_test(test_is_superuser, login_url=reverse_lazy("vug_failed_test", kwargs={'testname': "test_is_superuser", 'viewname': "vdev_testingview"}))
def vdev_testingview(request):
    viewname    = "vdev_testingview"
    zzz_print("    %-28s: %s" % ("viewname START", viewname))

    # Question from Alex
    dict1 = {'id': 161616, 'elements':[3333, '1']}
    x = y = z = None
    hop = {}

    for key, value in dict1.items():
        if key == "id":
            x = value
        elif key == "elements":
            y = value[0]
            z = value[1]
    if x and y and z:
        hop['x'] = x
        hop['y'] = y
        hop['z'] = z

    zzz_print("    %-28s: %s" % ("hop", hop))

    zzz_print("    %-28s: %s" % ("viewname END", viewname))
    return HttpResponseRedirect(reverse('vdev_home'))











































