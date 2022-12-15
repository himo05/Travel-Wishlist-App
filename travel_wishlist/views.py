from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

# Create your views here.

@login_required
def place_list(request):
    # This is the main view for the travel wishlist application. It allows users to
    # create new places and see a list of places they have not visited yet.
    if request.method == 'POST':
        #create new place
        # If the request is a POST request, create a new Place object using the
        # data from the NewPlaceForm form.
        form = NewPlaceForm(request.POST) # creating a form from data in the request
        place = form.save(commit=False) # creating a model oject from form
        place.user = request.user
        if form.is_valid(): # validation against DB constraints
            place.save()    # save place to db
            return redirect('place_list')   # relodes home page
            
            
    #places =Place.objects.all().order_by('name')
    #places=Place.objects.all()
    # Get a list of all the places in the database that have not been visited
    # and are associated with the current user, ordered 
    places =Place.objects.filter(user=request.user).filter(visited=False).order_by('name')
     # Create an instance of the NewPlaceForm form.
    new_place_form = NewPlaceForm() #used to create HTML
    return render(request,'travel_wishlist/wishlist.html',{'places':places,'new_place_form': new_place_form})

@login_required
def places_visited(request):
    # This view is used to display a list of places that the user has visited.
    # It gets a list of all the places in the database that have been visited.
    visited = Place.objects.filter(visited=True)
    # Render the visited.html template, passing in the list of visited places as context.
    return render(request,'travel_wishlist/visited.html',{'visited':visited})

@login_required
def place_was_visited(request, place_pk):
    # This view is used to mark a place as visited.
    if request.method == 'POST':
        # If the request is a POST request, get the Place object with the specified
        # primary key and update its visited status to True.
        place = get_object_or_404(Place, pk=place_pk)
        if place.user == request.user:
            place.visited = True
            place.save()
        else:
            # If the place does not belong to the current user, return a 403 Forbidden error.
            return HttpResponseForbidden()
    # Redirect the user back to the home page.
    return redirect('place_list')


@login_required
def place_details(request, place_pk):
    # This view is used to display the details of a place.
    # Get the Place object with the specified primary key.
    place = get_object_or_404(Place, pk=place_pk)
    # Render the place_details.html template, passing in the Place object as context.
    return render(request, 'travel_wishlist/place_details.html', {'place': place})


@login_required
def delete_place(request, place_pk):
    # This view is used to delete a place.
    # Get the Place object with the specified primary key.
    place = get_object_or_404(Place, pk=place_pk)
    if place.user == request.user:
        # If the place belongs to the current user, delete it.
        place.delete()
        # Redirect the user back to the home page.
        return redirect('place_list')
    else:
        # If the place does not belong to the current user, return a 403 Forbidden error.
        return HttpResponseForbidden


def about(request):
    # This view is used to display information about the travel wishlist application.
    author = 'Himo'
    about =  'A website to create a list of places to visit'
    # Render the about.html template, passing in the author and about information as context.
    return render(request,'travel_wishlist/about.html',{'author':author,'about':about})
    