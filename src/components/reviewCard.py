import json
import flet as ft
from components.authFunctions import submitReview
from components.alert import AlertBox

class LeaveReviewCard(ft.AlertDialog):
    def __init__(self, page, on_submit=None):
        self.on_submit = on_submit
        self.selected_rating = 0
        self.stars = []
        self.alert_box = AlertBox(page)
        self.page = page # Store the page reference

        self.review_input = ft.TextField(
            hint_text="Share your thoughts...",
            multiline=True,
            min_lines=3,
            max_lines=3,
            border_radius=8,
            filled=True,
            fill_color=ft.Colors.GREY_100,
            border_color=ft.Colors.GREY_300
        )

        self.submit_button = ft.ElevatedButton(
            "Submit Review",
            icon=ft.Icons.SEND,
            style=ft.ButtonStyle(
                padding=ft.padding.symmetric(horizontal=20, vertical=12),
                shape=ft.RoundedRectangleBorder(radius=8),
                bgcolor=ft.Colors.PURPLE_600,
                color=ft.Colors.WHITE,
            ),
            on_click=self.submit_review
        )

        self.star_row = ft.Row(
            controls=self.create_stars(),
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=4
        )

        super().__init__(
            modal=False,
            title=ft.Text("Leave a Review", size=20, weight=ft.FontWeight.BOLD),
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        
                        ft.Divider(),
                        self.star_row,
                        self.review_input,
                        ft.Container(height=12),
                        self.submit_button
                    ],
                spacing=3,horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),height=200,
            ),
            content_padding=ft.padding.symmetric(horizontal=10),
            shape=ft.RoundedRectangleBorder(radius=12),
            bgcolor=ft.Colors.WHITE,
        )

    def create_stars(self):
        self.stars.clear()
        self.stars = []
        for i in range(5):
            star = ft.IconButton(
                icon=ft.Icons.STAR_BORDER,
                icon_color=ft.Colors.GREY_500,
                data=i + 1,
                on_click=self.handle_star_click,
                tooltip=f"{i+1} Star{'s' if i > 0 else ''}"
            )
            self.stars.append(star)
        return self.stars

    def handle_star_click(self, e,reset=False):
        self.selected_rating = e.control.data if not reset else 0
        for i, star in enumerate(self.stars):
            star.icon = ft.Icons.STAR if i < self.selected_rating else ft.Icons.STAR_BORDER
            star.icon_color = ft.Colors.YELLOW_700 if i < self.selected_rating else ft.Colors.GREY_500
        self.update()

    def submit_review(self, e):
        review_text = self.review_input.value
        if not review_text:
            alert = AlertBox("Please enter a review and rating")
            if self.page: # Ensure page exists
                self.page.open(
                    alert
                )
            return
        elif self.selected_rating == 0:
            alert = AlertBox("Please enter a review and rating")
            if self.page: # Ensure page exists
                self.page.open(
                    alert
                )
            return
        
        try:
            # Get user_id from session
            session_user = None
            if self.page: # Ensure page exists before accessing session
                session_user = self.page.session.get("user")

            if session_user:
                user_data = json.loads(session_user)
                user_id = user_data.get("id")
            else:
                print("No user session found.")
                user_id = None

            # Submit to Supabase
            data = {
                "user_id": user_id,
                "text": review_text,
                "rating": self.selected_rating
            }
            alert = AlertBox("Submitted Feedback!")
            if self.page: # Ensure page exists
                self.page.open(
                    alert
                )
            response = submitReview(data)
            
            if response and response.data: # Ensure response is not None and has data
                print("Review submitted successfully.")
                if self.page: # Ensure page exists
                    self.page.close(alert)
                self.review_input.value = ""
                self.handle_star_click(e,reset=True)
                self.selected_rating = 0
                self.create_stars()  # Reset stars
                self.update()
            else:
                print(f"Error submitting review: {response.error if response else 'No response or data'}") # type: ignore
        except Exception as err:
            print(f"Unexpected error: {err}")
