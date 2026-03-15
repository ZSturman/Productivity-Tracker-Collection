//
//  ActionStateListView.swift
//  TrackingWell
//
//  Created by Zachary Sturman on 8/30/23.
//

import SwiftUI

struct ActionStateListView: View {
    @ObservedObject var viewModel: ActionStateListViewModel
    
    @State private var searchConfig: SearchConfig = .init()
    @State private var sort: Sort = .desc

    var body: some View {
        
        NavigationStack {
            List(viewModel.actionStates) { actionState in
                ActionStateRowView(actionState: actionState, viewModel: ActionStateDetailViewModel(actionState: actionState))
            }
            .navigationBarTitle("ActionStates")
            .searchable(text: $searchConfig.query)
            .navigationBarItems(
                trailing:
                    HStack {
                        Menu {
                            // Filter options
                            Button(action: { searchConfig.filter = .all }) {
                                Text("All")
                            }
                            Button(action: { searchConfig.filter = .action }) {
                                Text("Action")
                            }
                            Button(action: { searchConfig.filter = .state }) {
                                Text("State")
                            }
                            // Sort options
                            Button(action: { sort = .asc }) {
                                Text("Ascending")
                            }
                            Button(action: { sort = .desc }) {
                                Text("Descending")
                            }
                        } label: {
                            Image(systemName: "ellipsis.circle")
                        }
                    }
                )
            }

        .onChange(of: searchConfig) { newConfig in
            print(newConfig)
            //viewModel.actionStates.nsPredicate = ActionState.filter(with: newConfig)
        }
        .onChange(of: sort) { newSort in
            print(newSort)
            //viewModel.actionStates.nsSortDescriptors = ActionState.sort(order: newSort)
        }
    }
}


