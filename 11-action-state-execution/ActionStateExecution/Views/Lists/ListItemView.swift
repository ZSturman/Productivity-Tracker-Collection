//
//  ListItemView.swift
//  ActionStateExecution
//
//  Created by Zachary Sturman on 7/28/23.
//

import SwiftUI

struct ListItemView: View {
    let list: ListEntity
    @Environment(\.managedObjectContext) var managedObjectContext
    @FetchRequest(entity: ListItemEntity.entity(), sortDescriptors: []) var items: FetchedResults<ListItemEntity>
    
    @State private var newItemName: String = ""
    
    var body: some View {
        List {
            ForEach(items.filter { $0.list == list }, id: \.self) { item in
                Text(item.name ?? "")
            }
            .onDelete(perform: deleteItem)
            
            // New Item Input Field
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
        .navigationBarTitle(list.name ?? "", displayMode: .inline)
        .navigationBarItems(trailing: EditButton())
    }
    
    func deleteItem(at offsets: IndexSet) {
        for index in offsets {
            let item = items[index]
            managedObjectContext.delete(item)
        }
        
        do {
            try managedObjectContext.save()
        } catch {
            // handle the Core Data error
            print(error.localizedDescription)
        }
    }
    
    func addItem() {
        let newItem = ListItemEntity(context: managedObjectContext)
        newItem.name = newItemName
        newItem.list = list
        newItemName = ""
        
        do {
            try managedObjectContext.save()
        } catch {
            // handle the Core Data error
            print(error.localizedDescription)
        }
    }
}
