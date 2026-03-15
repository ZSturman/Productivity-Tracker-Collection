//
//  ContentView.swift
//  TrackingWell
//
//  Created by Zachary Sturman on 8/30/23.
//

import SwiftUI

struct ContentView: View {
    @State private var showingCreateEditView = false
    @FetchRequest(fetchRequest: ActionState.all()) private var actionStates

    var body: some View {
        NavigationStack {
            VStack {
                List {
                    ForEach(actionStates) { actionState in
                        Text(actionState.title ?? "")
                    }
                }
                if actionStates.isEmpty {
                    NoActionStateView()
                } else {
                    ActionStateListView(viewModel: ActionStateListViewModel())
                }
            }
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button(action: {
                        showingCreateEditView.toggle()
                    }, label: {
                        Image(systemName: "plus")
                    })
                }
            }
        }
        .sheet(isPresented: $showingCreateEditView) {
            CreateEditActionStateView(viewModel: CreateEditActionStateViewModel())
        }
    }
}
