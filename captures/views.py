from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import CapturedItem


@login_required
def capture_page(request):
    """
    Capture page for creating new items.

    Creates a new empty capture on GET, or loads existing capture if short_uuid provided.
    Route: /capture/ or /capture/<short_uuid>/

    Speed-first: Minimal server-side logic, page handles auto-save via API.
    """
    capture = None

    # If short_uuid in URL, load that capture
    short_uuid = request.GET.get('id')
    if short_uuid:
        try:
            capture = CapturedItem.objects.for_user(request.user).get(short_uuid=short_uuid)
        except CapturedItem.DoesNotExist:
            # Invalid UUID or not owned by user, redirect to new capture
            return redirect('capture')

    # If no capture provided, create a new one
    if not capture:
        capture = CapturedItem.objects.create(owner=request.user)
        # Redirect to same page with capture ID
        return redirect(f'/capture/?id={capture.short_uuid}')

    context = {
        'capture': capture,
        'images': capture.images.all(),
        'image_count': capture.images.count(),
    }

    return render(request, 'captures/capture.html', context)
