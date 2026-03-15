//
//  ListListView.swift
//  ActionStateExecution
//
//  Created by Zachary Sturman on 7/28/23.
//


import SwiftUI
import CoreData

struct ListListView: View {
    @State private var showNewList = false
    @Environment(\.managedObjectContext) var managedObjectContext
    @FetchRequest(entity: ListEntity.entity(), sortDescriptors: []) var lists: FetchedResults<ListEntity>
    
    var body: some View {

            List {
                ForEach(lists, id: \.self) { list in
                    NavigationLink(destination: ListItemView(list: list)) {
                        Text(list.name ?? "")
                    }
                }
            }
            .navigationBarTitle("Lists", displayMode: .inline)
            .navigationBarItems(trailing: Button(action: {
                self.showNewList = true
            }) {
                Image(systemName: "plus")
            })
            .sheet(isPresented: $showNewList) {
                NewListView().environment(\.managedObjectContext, self.managedObjectContext)
            }
        }
}

