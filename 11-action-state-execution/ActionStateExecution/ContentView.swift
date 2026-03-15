//
//  ContentView.swift
//  ActionStateExecution
//
//  Created by Zachary Sturman on 7/27/23.
//
import SwiftUI

struct ContentView: View {
    @Environment(\.managedObjectContext) var managedObjectContext
    
    @FetchRequest(
        entity: ActionStateEntity.entity(),
        sortDescriptors: [
            NSSortDescriptor(keyPath: \ActionStateEntity.name, ascending: true),
        ]
    ) var actionStates: FetchedResults<ActionStateEntity>
    
    @FetchRequest(
        entity: TopicsEntity.entity(),
        sortDescriptors: [
            NSSortDescriptor(keyPath: \TopicsEntity.name, ascending: true),
        ]
    ) var topics: FetchedResults<TopicsEntity>
    
    var body: some View {
        NavigationView {
            ScrollView {
                ActionStatesListView(actionStates: actionStates)
            }
            .navigationBarTitle("Home")
            .toolbar {
                ToolbarItemGroup(placement: .navigationBarTrailing) {
                    NavigationLink(destination: CreateActionStateView(actionStateViewModel: ActionStateViewModel(context: self.managedObjectContext))) {
                        Text("Add")
                    }
                }
                ToolbarItemGroup(placement: .navigationBarLeading) {
                    NavigationLink(destination: UserSettingsView()) {
                        Text(Image(systemName: "person.circle"))
                    }
                }
            }
        }
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        NavigationView {
            ContentView()
        }
    }
}
