//
//  NewListView.swift
//  ActionStateExecution
//
//  Created by Zachary Sturman on 7/28/23.

import SwiftUI
import CoreData

struct NewListView: View {
    @State private var listName: String = ""
    @State private var itemNames: [String] = [""]
    @Environment(\.presentationMode) var presentationMode
    @Environment(\.managedObjectContext) var managedObjectContext
    @State private var newItemName: String = ""
    
    var body: some View {
        NavigationView {
            Form {
                Section(header: Text("List Name")) {
                    TextField("New List", text: $listName)
                }

                Section(header: Text("List Items")) {
                    ForEach(0..<itemNames.count, id: \.self) { index in
                        TextField("New List Item", text: $itemNames[index])
                    }
                    .onDelete(perform: deleteItem) // To delete an item
                    
                    HStack {
                        TextField("New Item", text: $newItemName)
                        Button(action: {
                            addItem()
                        }) {
                            Image(systemName: "plus.circle.fill")
                                .foregroundColor(.green)
                        }
                    }
                }
                
                Button(action: {
                    saveList()
                }) {
                    Text("Save")
                }
                .disabled(listName.isEmpty)
            }
            .navigationBarTitle("\(listName)", displayMode: .inline)
            .navigationBarItems(trailing: EditButton())
        }
    }
    
    func deleteItem(at offsets: IndexSet) {
        for index in offsets {
            itemNames.remove(at: index)
        }
    }
    
    func addItem() {
        itemNames.append(newItemName)
        newItemName = ""
    }
    
    func saveList() {
        let newList = ListEntity(context: self.managedObjectContext)
        newList.id = UUID()
        newList.name = self.listName
        
        for itemName in self.itemNames {
            let newListItem = ListItemEntity(context: self.managedObjectContext)
            newListItem.id = UUID()
            newListItem.name = itemName
            newListItem.list = newList
        }
        
        try? self.managedObjectContext.save()
        self.presentationMode.wrappedValue.dismiss()
    }
}
