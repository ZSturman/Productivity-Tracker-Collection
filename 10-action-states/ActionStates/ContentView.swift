//
//  ContentView.swift
//  ActionStates
//
//  Created by Zachary Sturman on 7/22/23.
//

import SwiftUI

struct ContentView: View {
    @EnvironmentObject var listViewModel: ListsViewModel
    @ObservedObject var listItemViewModel: ListItemViewModel

    var body: some View {
        NavigationView {
            VStack {
                List {
                    NavigationLink {
                        AddListView()
                    } label: {
                        Text("Lists")
                    }
                }
                ListListView()
                    .environmentObject(listItemViewModel)
            }
            .navigationTitle("Home")
            .toolbar {
                ToolbarItem(placement: .navigationBarLeading){
                    Button {
                        
                    } label : {
                        Label("Profile", systemImage: "person.circle")
                    }
                }
            }
        }
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        // Creating a mock data controller, lists view model, and list item view model
        let dataController = DataController()
        let listsViewModel = ListsViewModel(container: dataController.container)
        let listItemViewModel = ListItemViewModel(container: dataController.container)

        ContentView(listItemViewModel: listItemViewModel)
            .environmentObject(listsViewModel)
    }
}
