#!/usr/bin/env python3
"""
Helpdesk System - Service Desk Ticket Management
Simple terminal application for Part V Kanban practice

This system demonstrates an "existing codebase" scenario where basic
functionality already works, but needs ongoing maintenance and enhancements.
Students will apply Kanban practices to manage continuous flow of work items.
"""

import datetime
from typing import List, Dict, Optional

# Global data structures
tickets: List[Dict] = []
default_priorities = ""
priority_levels = []
default_categories = ""
categories_list = []
ticket_counter = 1

# Starter tickets (demonstrates existing system with some data)
def initialize_starter_data():
    """Initialize system with 3 existing tickets to demonstrate 'existing codebase' concept"""
    global tickets, priority_levels, ticket_counter, categories_list

    tickets = [
        {
            'id': 1,
            'title': 'Cannot access shared drive',
            'description': 'User reports unable to connect to //fileserver/shared. Getting "access denied" error.',
            'priority': 'High',
            'category': 'Access',
            'status': 'Open',
            'assigned_to': 'Support Team',
            'created_at': datetime.datetime.now() - datetime.timedelta(days=2),
            'comments': ['Initial report received from user@example.com']
        },
        {
            'id': 2,
            'title': 'Printer not working in Room 301',
            'description': 'HP LaserJet in Room 301 showing error code 49. Paper jams frequently.',
            'priority': 'Medium',
            'category': 'Hardware',
            'status': 'In Progress',
            'assigned_to': 'Alice Johnson',
            'created_at': datetime.datetime.now() - datetime.timedelta(days=1),
            'comments': ['Ticket assigned to Alice', 'Alice: Checked printer, ordered replacement parts']
        },
        {
            'id': 3,
            'title': 'Email not syncing on mobile device',
            'description': 'User cannot receive emails on iPhone. Webmail works fine.',
            'priority': 'Low',
            'category': 'Software',
            'status': 'Closed',
            'assigned_to': 'Bob Smith',
            'created_at': datetime.datetime.now() - datetime.timedelta(days=3),
            'comments': ['Bob: Reset mobile sync settings', 'Bob: Issue resolved, user confirmed emails working']
        }
    ]

    priority_levels = ['Low', 'Medium', 'High']
    default_priorities = "Medium"
    categories_list = ['Hardware', 'Software', 'Network', 'Access', 'Other']
    default_categories = "None"

    ticket_counter = 4  # Next ticket will be ID 4


def create_ticket() -> None:
    """Create a new support ticket"""
    global ticket_counter

    print("\n=== Create New Ticket ===")
    title = input("Ticket title: ").strip()
    if not title:
        print("Error: Title cannot be empty")
        return

    description = input("Description: ").strip()
    if not description:
        print("Error: Description cannot be empty")
        return
    
    # Select priority
    priority = ask_for_ListData("Priority", priority_levels, default_priorities)
    if not priority:
        print("Error: Invalid priority selection")
        return
    
    # Select category
    category = ask_for_ListData("Category", categories_list, default_categories)
    if not category:
        print("Error: Invalid category selection")
        return

    # Create new ticket
    new_ticket = {
        'id': ticket_counter,
        'title': title,
        'description': description,
        'priority': priority,
        'category': category,
        'status': 'Open',
        'assigned_to': 'Unassigned',
        'created_at': datetime.datetime.now(),
        'comments': []
    }

    tickets.append(new_ticket)
    print(f"\n✓ Ticket #{ticket_counter} created successfully")
    ticket_counter += 1

def ask_for_ListData(name: str, lst: list, default: str = "None") -> str:
    """
    Ask user to select an item from a list\n
    if list is not defined, returns 'Medium'\n
    if user answer is invalid, returns None
    """
    if len(lst) == 0:
        return default
    else:
        print(f"{name} levels:")
        for i in range(len(lst)):
            print(f"{i + 1}. {lst[i]}")

        selection = input(f"select {name} (1-{len(lst)}): ").strip()
        if not selection.isdigit() or not (1 <= int(selection) <= len(lst)):
            return None
        return lst[int(selection) - 1]

def view_tickets(filter_status: Optional[str] = None, filter_priority: Optional[str] = None, filter_category: Optional[str] = None) -> None:
    """
    View all tickets or filtered by status

    Args:
        filter_status: Optional status filter ('Open', 'In Progress', 'Closed')
    """
    print("\n=== Ticket List ===")

    # Filter tickets by status if specified
    filtered_tickets = tickets
    redacted_filter_status = ticket_status_redact(filter_status)
    if filter_status:
        filtered_tickets = [t for t in tickets if t['status'] == redacted_filter_status]
        print(f"Filter: '{redacted_filter_status}' tickets only")
    
    if filter_priority:
        filtered_tickets = [t for t in filtered_tickets if t['priority'] == filter_priority]
        print(f"Filter: '{filter_priority}' priority tickets only")

    if filter_category:
        filtered_tickets = [t for t in filtered_tickets if t['category'] == filter_category]
        print(f"Filter: '{filter_category}' category tickets only")

    if not filtered_tickets:
        print("No tickets found")
        return

    # Display tickets in table format
    print(f"\n{'ID':<5} {'Title':<30} {'Priority':<10} {'Category':<15} {'Status':<15} {'Assigned To':<20} {'Created':<12}")
    print("-" * 110)

    for ticket in filtered_tickets:
        created_str = ticket['created_at'].strftime('%Y-%m-%d')
        title_truncated = ticket['title'][:28] + '..' if len(ticket['title']) > 30 else ticket['title']

        print(f"{ticket['id']:<5} {title_truncated:<30} {ticket['priority']:<10} {ticket['category']:<15} {ticket['status']:<15} "
              f"{ticket['assigned_to']:<20} {created_str:<12}")

    print(f"\nTotal: {len(filtered_tickets)} tickets")

def ticket_status_redact(status: str) -> str:
    """
    Redacts ticket status, to make them suitable for using in system\n
    removing whitespaces and make every word capitalized\n
    If given none, returns none
    """
    if not status:
        return None
    status_list = status.strip().split(" ")
    for i in range(len(status_list)):
        status_list[i] = status_list[i].capitalize()
    new_status = " ".join(status_list)
    return new_status
    

def view_ticket_details(ticket_id: int) -> None:
    """View full details of a specific ticket"""
    ticket = find_ticket_by_id(ticket_id)
    if not ticket:
        print(f"Error: Ticket #{ticket_id} not found")
        return

    print("\n" + "=" * 60)
    print(f"Ticket #{ticket['id']}: {ticket['title']}")
    print("=" * 60)
    print(f"Priority: {ticket['priority']}")
    print(f"Category: {ticket['category']}")
    print(f"Status: {ticket['status']}")
    print(f"Assigned To: {ticket['assigned_to']}")
    print(f"Created: {ticket['created_at'].strftime('%Y-%m-%d %H:%M')}")
    print(f"\nDescription:\n{ticket['description']}")

    if ticket['comments']:
        print(f"\nComments ({len(ticket['comments'])}):")
        for i, comment in enumerate(ticket['comments'], 1):
            print(f"  {i}. {comment}")
    else:
        print("\nNo comments yet")
    print("=" * 60)


def assign_ticket(ticket_id: int, staff_name: str) -> None:
    """
    Assign ticket to support staff

    Args:
        ticket_id: ID of ticket to assign
        staff_name: Name of staff member to assign to
    """
    ticket = find_ticket_by_id(ticket_id)
    if not ticket:
        print(f"Error: Ticket #{ticket_id} not found")
        return

    if not validate_staff_name(staff_name):
        print("Error: Invalid staff name. Please enter a valid name without special characters or numbers.")
        return

    ticket['assigned_to'] = redact_staff_name(staff_name)
    ticket['comments'].append(f"Ticket assigned to {staff_name}")

    # Auto-change status to In Progress if currently Open
    if ticket['status'] == 'Open':
        ticket['status'] = 'In Progress'

    print(f"\n✓ Ticket #{ticket_id} assigned to {staff_name}")

def validate_staff_name(name: str) -> bool:
    """
    Validates, that staff name is acceptable to use.
    """
    banned_strings = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "[", "]", "{", "}", "(", ")", "<", ">", "/", "\\", "|", "@", "#", "$", "%", "^", "&", "*", "!", "~", '"',]

    if len(name.strip()) == 0:
        return False
    if name.isdigit():
        return False
    if any(banned in name.lower() for banned in banned_strings):
        return False
    return True

def redact_staff_name(name: str) -> str:
    """
    redacts staff name, to make them suitable for reading
    """
    name_lst = name.split(" ")
    new_name = ""
    for i in range(len(name_lst)):
        name_lst[i] = name_lst[i].capitalize()
    new_name = " ".join(name_lst)
    return new_name

def add_comment(ticket_id: int, comment: str) -> None:
    """
    Add comment/update to ticket

    Args:
        ticket_id: ID of ticket
        comment: Comment text to add
    """
    ticket = find_ticket_by_id(ticket_id)
    if not ticket:
        print(f"Error: Ticket #{ticket_id} not found")
        return

    if not comment.strip():
        print("Error: Comment cannot be empty")
        return

    ticket['comments'].append(comment)
    print(f"\n✓ Comment added to ticket #{ticket_id}")


def close_ticket(ticket_id: int) -> None:
    """
    Close a ticket (mark as resolved)

    Args:
        ticket_id: ID of ticket to close
    """
    ticket = find_ticket_by_id(ticket_id)
    if not ticket:
        print(f"Error: Ticket #{ticket_id} not found")
        return

    if ticket['status'] == 'Closed':
        print(f"Ticket #{ticket_id} is already closed")
        return

    ticket['status'] = 'Closed'
    ticket['comments'].append(f"Ticket closed")
    print(f"\n✓ Ticket #{ticket_id} closed successfully")


def search_tickets(query: str) -> None:
    """
    Search tickets by ID or title

    Args:
        query: Search query (ticket ID number or title keywords)
    """
    print(f"\n=== Search Results for '{query}' ===")

    # Try to search by ID first
    if query.strip().isdigit():
        ticket_id = int(query)
        ticket = find_ticket_by_id(ticket_id)
        if ticket:
            view_ticket_details(ticket_id)
            return

    # Search by title (case-insensitive)
    query_lower = query.lower()
    matching_tickets = [t for t in tickets if query_lower in t['title'].lower()
                        or query_lower in t['description'].lower()]

    if not matching_tickets:
        print("No tickets found matching query")
        return

    # Display matching tickets
    print(f"\n{'ID':<5} {'Title':<30} {'Priority':<10} {'Category':<15} {'Status':<15} {'Assigned To':<20}")
    print("-" * 95)

    for ticket in matching_tickets:
        title_truncated = ticket['title'][:28] + '..' if len(ticket['title']) > 30 else ticket['title']
        print(f"{ticket['id']:<5} {title_truncated:<30} {ticket['priority']:<10} {ticket['category']:<15} {ticket['status']:<15} {ticket['assigned_to']:<20}")

    print(f"\nFound {len(matching_tickets)} matching tickets")


def find_ticket_by_id(ticket_id: int) -> Optional[Dict]:
    """
    Find ticket by ID

    Args:
        ticket_id: Ticket ID to search for

    Returns:
        Ticket dictionary if found, None otherwise
    """
    for ticket in tickets:
        if ticket['id'] == ticket_id:
            return ticket
    return None


def main_menu() -> None:
    """Main menu loop"""
    print("\n" + "=" * 60)
    print("  HELPDESK SYSTEM - Service Desk Ticket Management")
    print("=" * 60)
    print("  Part V Kanban Practice - Existing Codebase Scenario")
    print("=" * 60)

    while True:
        print("\n--- Main Menu ---")
        print("1. View all tickets")
        print("2. View open tickets only")
        print("3. View ticket details")
        print("4. Create new ticket")
        print("5. Assign ticket")
        print("6. Add comment to ticket")
        print("7. Close ticket")
        print("8. Search tickets")
        print("9. Search tickets by priority")
        print("10. Search tickets by category")
        print("0. Exit")

        choice = input("\nSelect option: ").strip()

        if choice == '1':
            view_tickets()

        elif choice == '2':
            view_tickets(filter_status='Open')

        elif choice == '3':
            try:
                ticket_id = int(input("Enter ticket ID: "))
                view_ticket_details(ticket_id)
            except ValueError:
                print("Error: Invalid ticket ID")

        elif choice == '4':
            create_ticket()

        elif choice == '5':
            try:
                ticket_id = int(input("Enter ticket ID: "))
                staff_name = input("Assign to (staff name): ").strip()
                if staff_name:
                    assign_ticket(ticket_id, staff_name)
                else:
                    print("Error: Staff name cannot be empty")
            except ValueError:
                print("Error: Invalid ticket ID")

        elif choice == '6':
            try:
                ticket_id = int(input("Enter ticket ID: "))
                comment = input("Comment: ").strip()
                if comment:
                    add_comment(ticket_id, comment)
            except ValueError:
                print("Error: Invalid ticket ID")

        elif choice == '7':
            try:
                ticket_id = int(input("Enter ticket ID: "))
                close_ticket(ticket_id)
            except ValueError:
                print("Error: Invalid ticket ID")

        elif choice == '8':
            query = input("Search query (ID or keywords): ").strip()
            if query:
                search_tickets(query)

        elif choice == '9':
            priority = ask_for_ListData("Priority", priority_levels, default_priorities)
            if priority:
                view_tickets(filter_priority=priority)
            else:
                print("Error: Invalid priority selection")

        elif choice == '10':
            category = ask_for_ListData("Category", categories_list, default_categories)
            if category:
                view_tickets(filter_category=category)
            else:
                print("Error: Invalid category selection")

        elif choice == '0':
            print("\n👋 Thank you for using Helpdesk System!")
            break

        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    # Initialize with starter data
    initialize_starter_data()

    # Run main menu
    main_menu()
