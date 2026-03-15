//
//  ListDetailedView.swift
//  ActionStates
//
//  Created by Zachary Sturman on 7/27/23.
//

import SwiftUI

struct ListDetailedView: View {
    @ObservedObject var listItemViewModel: ListItemViewModel
    let list: ListEntity
    @State private var listItemName: String = ""
    
    var body: some View {
        VStack {
            TextField("New Item", text: $listItemName)
            Button("Add Item") {
                listItemViewModel.addListItem(listItem: listItemName, to: list)
                listItemName = ""
            }
            List(listItemViewModel.listItems, id: \.self) { item in
                Text(item.name ?? "")
            }
        }
        .onAppear {
            listItemViewModel.fetchListItems(for: list)
        }
    }
}
