//
//  ActionStateListView.swift
//  ActionStates
//
//  Created by Zachary Sturman on 7/23/23.
//

import SwiftUI


struct ActionStateListView: View {
    @Environment(\.managedObjectContext) var moc

    @FetchRequest(
        entity: ActionStateEntity.entity(),
        sortDescriptors: [NSSortDescriptor(keyPath: \ActionStateEntity.name, ascending: true)]
    ) var actionStates: FetchedResults<ActionStateEntity>

    var body: some View {
        List(actionStates, id: \.id) { actionState in
            NavigationLink {
                ActionStateDetailedView(actionState: actionState)
                    .environment(\.managedObjectContext, self.moc)
            } label: {
                Text(actionState.name ?? "")
            }
        }
        .navigationTitle("Action States")
        .toolbar {
            ToolbarItem(placement: .navigationBarTrailing) {
                NavigationLink {
                    AddActionStateFormView(moc: self.moc)
                        .environment(\.managedObjectContext, self.moc)
                } label: {
                    Label("Add", systemImage: "plus")
                }

            }
        }
    }
}


