from fastapi import status

def test_get_activities(client):
    """Test getting the list of activities"""
    response = client.get("/activities")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), dict)
    # Verificar que las actividades tienen la estructura correcta
    for activity in response.json().values():
        assert "description" in activity
        assert "schedule" in activity
        assert "max_participants" in activity
        assert "participants" in activity

def test_signup_for_activity(client):
    """Test signing up for an activity"""
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    
    # Intentar registrarse
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == status.HTTP_200_OK
    assert "message" in response.json()
    assert email in response.json()["message"]

    # Verificar que el estudiante aparece en la lista de participantes
    activities = client.get("/activities").json()
    assert email in activities[activity_name]["participants"]

def test_signup_duplicate(client):
    """Test that a student cannot sign up twice for the same activity"""
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Un estudiante que ya está registrado
    
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "already signed up" in response.json()["detail"]

def test_signup_nonexistent_activity(client):
    """Test signing up for a non-existent activity"""
    response = client.post("/activities/NonexistentClub/signup?email=test@mergington.edu")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "not found" in response.json()["detail"]

def test_unregister_from_activity(client):
    """Test unregistering from an activity"""
    activity_name = "Chess Club"
    email = "daniel@mergington.edu"  # Un estudiante que está registrado
    
    # Intentar darse de baja
    response = client.post(f"/activities/{activity_name}/unregister?email={email}")
    assert response.status_code == status.HTTP_200_OK
    assert "message" in response.json()
    assert email in response.json()["message"]

    # Verificar que el estudiante ya no aparece en la lista
    activities = client.get("/activities").json()
    assert email not in activities[activity_name]["participants"]

def test_unregister_not_signed_up(client):
    """Test unregistering when not signed up"""
    activity_name = "Chess Club"
    email = "notsignedup@mergington.edu"
    
    response = client.post(f"/activities/{activity_name}/unregister?email={email}")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "not signed up" in response.json()["detail"]