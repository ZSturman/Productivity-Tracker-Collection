//
//  UserSettingsView.swift
//  ActionStateExecution
//
//  Created by Zachary Sturman on 7/28/23.
//

import SwiftUI

struct UserSettingsView: View {
    
    @State private var notificationsEnabled = true
    @State private var email = "user@example.com"
    @State private var username = "username"
    
    var body: some View {

            Form {
                Section(header: Text("Profile")) {
                    TextField("Username", text: $username)
                    TextField("Email", text: $email)
                }
                
                Section(header: Text("Notifications")) {
                    Toggle(isOn: $notificationsEnabled) {
                        Text("Enable Notifications")
                    }
                }
                
                Section(header: Text("My Lists")) {
                    List {
                        
//                        NavigationLink(destination: NewTopicView()) {
//                            Text("Topics")
//                        }
                        
                        NavigationLink(destination: NewTagView()) {
                            Text("Tags")
                        }
                        
                        NavigationLink(destination: ListListView()) {
                            Text("Lists")
                        }
                    }
                    
                }
                
                Section(header: Text("Account Actions")) {
                    Button("Change Password") {
                        print("Change password")
                    }
                    
                    Button("Logout") {
                        print("Logout")
                    }
                }
            }
            .navigationBarTitle("Settings")
        }

}

struct UserSettingsView_Previews: PreviewProvider {
    static var previews: some View {
        NavigationView {
            UserSettingsView()
        }
    }
}
