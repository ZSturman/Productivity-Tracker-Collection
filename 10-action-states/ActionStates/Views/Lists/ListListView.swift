//
//  ListListView.swift
//  ActionStates
//
//  Created by Zachary Sturman on 7/27/23.
//

import SwiftUI


struct ListListView: View {
    @EnvironmentObject var listViewModel: ListsViewModel
    @EnvironmentObject var listItemViewModel: ListItemViewModel

    var body: some View {
        List {
            ForEach(listViewModel.lists, id: \.self) { list in
                NavigationLink {
                    ListDetailedView(listItemViewModel: listItemViewModel, list: list)
                } label: {
                    Text(list.name ?? "")
                }
            }
        }
        .navigationTitle("Lists")
    }
}
